"""
自动化评审流水线

完整流程：
1. 读取原始论文 Markdown
2. 读取相关文献摘要
3. 调用 LLM 生成结构化评审报告
4. 保存评审报告
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from literature_review.logger import get_logger

logger = get_logger("review_pipeline")

# 导入已有的模块
sys.path.append(str(Path(__file__).parent.parent))
from literature_review.review_generator import ReviewGenerator


def run_review_generation(
    paper_id: str,
    language: str = "chinese",
    input_dir: str = None
):
    """
    运行评审生成流水线
    
    Args:
        paper_id: 论文ID
        language: 评审语言 ('chinese' 或 'english')
        input_dir: 输入目录（默认为 pipeline/literature_search_results）
    """
    logger.info("═" * 70)
    logger.info("📝 自动化评审报告生成流水线")
    logger.info("═" * 70)
    logger.info(f"论文 ID: {paper_id} | 评审语言: {language}")
    
    # 设置路径
    if input_dir is None:
        input_dir = Path(__file__).parent / "literature_search_results"
    else:
        input_dir = Path(input_dir)
    
    paper_dir = input_dir / paper_id
    
    # 检查输入目录
    if not paper_dir.exists():
        logger.error(f"找不到论文目录 {paper_dir}")
        logger.error("请先运行前面的流程（文献检索和相关度打分）")
        return
    
    # ===== 第 1 步: 加载原始论文 =====
    logger.info("═" * 70)
    logger.info("第 1 步: 加载原始论文")
    logger.info("═" * 70)
    
    # 查找原始论文的 Markdown 文件
    source_md_path = None
    
    # 尝试多个可能的位置
    possible_paths = [
        paper_dir / f"{paper_id}_source.md",  # literature_search_pipeline 保存的位置
        Path(__file__).parent / "outputs" / paper_id / "full.md",  # mineru_pipeline 输出位置
    ]
    
    for path in possible_paths:
        if path.exists():
            source_md_path = path
            break
    
    if not source_md_path:
        logger.error("找不到原始论文的 Markdown 文件")
        logger.error("尝试过的路径:")
        for p in possible_paths:
            logger.error(f"  - {p}")
        return
    
    logger.info(f"✅ 找到原始论文: {source_md_path}")
    
    with open(source_md_path, 'r', encoding='utf-8') as f:
        source_md = f.read()
    
    logger.info(f"长度: {len(source_md)} 字符")
    
    # 加载元数据
    metadata_path = paper_dir / "metadata.json"
    with open(metadata_path, 'r', encoding='utf-8') as f:
        source_metadata = json.load(f)
    
    logger.info(f"标题: {source_metadata['title']}")
    
    # ===== 第 2 步: 加载相关文献摘要 =====
    logger.info("═" * 70)
    logger.info("第 2 步: 加载相关文献摘要")
    logger.info("═" * 70)
    
    # 从 ranked_papers.json 获取高相关度论文列表
    ranked_path = paper_dir / "ranked_papers.json"
    
    if not ranked_path.exists():
        logger.error("找不到 ranked_papers.json")
        logger.error("请先运行 ranking_and_summary_pipeline.py")
        return
    
    with open(ranked_path, 'r', encoding='utf-8') as f:
        ranked_data = json.load(f)
    
    high_rel_papers = ranked_data.get('high_relevance', [])
    logger.info(f"高相关度论文数: {len(high_rel_papers)}")
    
    # 读取每篇论文的详细摘要
    related_summaries = []
    high_rel_dir = paper_dir / "high_relevance"
    
    for item in high_rel_papers:
        arxiv_id = item['arxiv_id']
        summary_path = high_rel_dir / arxiv_id / "detailed_summary.md"
        
        if summary_path.exists():
            with open(summary_path, 'r', encoding='utf-8') as f:
                # 跳过元数据头部，只读取摘要内容
                content = f.read()
                # 提取 "# 对比摘要" 后的内容
                if "# 对比摘要" in content:
                    summary = content.split("# 对比摘要", 1)[1].strip()
                else:
                    summary = content
                
            related_summaries.append({
                'arxiv_id': arxiv_id,
                'title': item['title'],
                'score': item['score'],
                'summary': summary
            })
            logger.info(f"✅ 加载摘要: {arxiv_id}")
        else:
            logger.warning(f"未找到摘要: {arxiv_id}")
    
    logger.info(f"成功加载 {len(related_summaries)} 篇高相关度文献摘要")
    
    # 加载低相关度论文摘要
    low_rel_path = paper_dir / "low_relevance_summaries.json"
    low_rel_summaries = []
    if low_rel_path.exists():
        with open(low_rel_path, 'r', encoding='utf-8') as f:
            low_rel_summaries = json.load(f)
        logger.info(f"低相关度论文数: {len(low_rel_summaries)}")
        for item in low_rel_summaries:
            related_summaries.append({
                'arxiv_id': item['arxiv_id'],
                'title': item['title'],
                'score': item['score'],
                'summary': item['summary']
            })
    else:
        logger.warning("未找到低相关度摘要文件，仅使用高相关度文献")
    
    logger.info(f"总计 {len(related_summaries)} 篇文献参与评审")
    
    # ===== 第 3 步: 生成评审报告 =====
    logger.info("═" * 70)
    logger.info("第 3 步: 生成评审报告")
    logger.info("═" * 70)
    
    generator = ReviewGenerator()
    
    review = generator.generate_review(
        source_md,
        source_metadata,
        related_summaries,
        language=language
    )
    

    
    # ===== 第 4 步: 保存评审报告 =====
    logger.info("═" * 70)
    logger.info("第 4 步: 保存评审报告")
    logger.info("═" * 70)
    
    # 保存评审报告
    review_filename = f"review_report_{language}.md"
    review_path = paper_dir / review_filename
    
    review_metadata = {
        'title': source_metadata['title'],
        'authors': source_metadata.get('authors', []),
        'num_related_papers': len(related_summaries),
        'language': language
    }
    
    generator.save_review(review, review_path, metadata=review_metadata)
    
    # 保存元数据
    review_meta_path = paper_dir / "review_metadata.json"
    with open(review_meta_path, 'w', encoding='utf-8') as f:
        json.dump({
            'paper_id': paper_id,
            'generated_at': datetime.now().isoformat(),
            'language': language,
            'num_related_papers': len(related_summaries),
            'review_file': review_filename
        }, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ 元数据已保存: {review_meta_path}")

    logger.info("═" * 70)
    logger.info("✅ 完成！评审报告已生成")
    logger.info("═" * 70)
    logger.info(f"📄 评审报告: {review_path.resolve()}")
    logger.info(f"📊 元数据: {review_meta_path.resolve()}")
    logger.info("建议：查看评审报告并根据需要调整")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='自动化评审报告生成流水线'
    )
    
    parser.add_argument(
        'paper_id',
        help='论文ID（例如：2401.12345）'
    )
    
    parser.add_argument(
        '-l', '--language',
        choices=['chinese', 'english'],
        default='chinese',
        help='评审语言（默认: chinese）'
    )
    
    parser.add_argument(
        '-i', '--input-dir',
        default=None,
        help='输入目录（默认: pipeline/literature_search_results）'
    )
    
    args = parser.parse_args()
    
    run_review_generation(
        paper_id=args.paper_id,
        language=args.language,
        input_dir=args.input_dir
    )


if __name__ == '__main__':
    main()
