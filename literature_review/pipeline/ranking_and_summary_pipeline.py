"""
相关度打分和摘要生成流水线

完整流程：
1. 读取文献检索结果
2. 计算相关度分数
3. 筛选 top-k 高相关度论文
4. 对高相关度论文：下载 PDF → 转 MD → 生成详细摘要
5. 对低相关度论文：使用原摘要
6. 生成综合报告
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from literature_review.logger import get_logger

logger = get_logger("ranking_and_summary_pipeline")

# 导入已有的模块
sys.path.append(str(Path(__file__).parent.parent))
from literature_review.relevance_scorer import RelevanceScorer
from literature_review.pdf_processor import PDFProcessor
from literature_review.summary_generator import SummaryGenerator


def run_ranking_and_summary(
    paper_id: str,
    top_k: int = 15,
    language: str = "chinese",
    input_dir: str = None
):
    """
    运行相关度打分和摘要生成流水线
    
    Args:
        paper_id: 论文ID
        top_k: 高相关度论文数量
        language: 摘要语言 ('chinese' 或 'english')
        input_dir: 输入目录（默认为 pipeline/literature_search_results）
    """
    logger.info("═" * 70)
    logger.info("📊 相关度打分和摘要生成流水线")
    logger.info("═" * 70)
    logger.info(f"论文 ID: {paper_id} | Top-K: {top_k} | 摘要语言: {language}")
    
    # 设置路径
    if input_dir is None:
        input_dir = Path(__file__).parent / "literature_search_results"
    else:
        input_dir = Path(input_dir)
    
    paper_dir = input_dir / paper_id
    
    # 检查输入目录
    if not paper_dir.exists():
        logger.error(f"找不到论文目录 {paper_dir}")
        logger.error("请先运行 literature_search_pipeline.py")
        return
    
    # ===== 第 1 步: 加载数据 =====
    logger.info("═" * 70)
    logger.info("第 1 步: 加载数据")
    logger.info("═" * 70)
    
    # 加载源论文元数据
    metadata_path = paper_dir / "metadata.json"
    with open(metadata_path, 'r', encoding='utf-8') as f:
        source_metadata = json.load(f)
    
    logger.info(f"源论文: {source_metadata['title']}")
    
    # 加载候选论文列表
    results_path = paper_dir / "arxiv_results.json"
    with open(results_path, 'r', encoding='utf-8') as f:
        candidate_papers = json.load(f)
    
    logger.info(f"候选论文数: {len(candidate_papers)}")
    
    # ===== 第 2 步: 计算相关度 =====
    logger.info("═" * 70)
    logger.info("第 2 步: 计算相关度分数")
    logger.info("═" * 70)
    
    scorer = RelevanceScorer()
    scored_papers = scorer.score_papers(source_metadata, candidate_papers)
    
    # 保存评分结果
    scores_path = paper_dir / "relevance_scores.json"
    scorer.save_scores(scored_papers, scores_path)

    
    # ===== 第 3 步: 筛选论文 =====
    logger.info("═" * 70)
    logger.info("第 3 步: 筛选高相关度论文")
    logger.info("═" * 70)
    
    high_rel, low_rel = scorer.select_top_k(scored_papers, k=top_k)
    
    # 保存排序后的论文列表
    ranked_papers = {
        'high_relevance': [
            {
                'arxiv_id': p.get('arxiv_id', p.get('id')),
                'title': p['title'],
                'score': float(score),
                'authors': p.get('authors', [])[:3],
                'published': p.get('published', '')
            }
            for p, score in high_rel
        ],
        'low_relevance': [
            {
                'arxiv_id': p.get('arxiv_id', p.get('id')),
                'title': p['title'],
                'score': float(score)
            }
            for p, score in low_rel
        ]
    }
    
    ranked_path = paper_dir / "ranked_papers.json"
    with open(ranked_path, 'w', encoding='utf-8') as f:
        json.dump(ranked_papers, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ 排序结果已保存: {ranked_path}")
    
    # ===== 第 4 步: 处理高相关度论文 =====
    logger.info("═" * 70)
    logger.info("第 4 步: 处理高相关度论文")
    logger.info("═" * 70)
    
    high_rel_dir = paper_dir / "high_relevance"
    high_rel_dir.mkdir(exist_ok=True)
    
    processor = PDFProcessor()
    generator = SummaryGenerator()
    
    high_rel_summaries = []
    
    for i, (paper, score) in enumerate(high_rel, 1):
        arxiv_id = paper.get('arxiv_id', paper.get('id'))
        logger.info(f"[{i}/{len(high_rel)}] 处理: {arxiv_id}")
        logger.info(f"  标题: {paper['title'][:60]}...")
        logger.info(f"  相关度: {score:.3f}")
        
        paper_output_dir = high_rel_dir / arxiv_id
        
        # 1) 下载并转换 PDF
        pdf_path = processor.download_pdf(arxiv_id, paper_output_dir)
        
        if pdf_path:
            md_path = processor.convert_pdf_to_markdown(pdf_path, paper_output_dir)
        else:
            md_path = None
        
        # 2) 生成摘要
        if md_path and md_path.exists():
            # 读取 Markdown
            with open(md_path, 'r', encoding='utf-8') as f:
                candidate_md = f.read()
            
            # 生成详细摘要
            summary = generator.generate_detailed_summary(
                source_metadata,
                paper,
                candidate_md,
                language=language
            )
        else:
            logger.warning("PDF 转换失败，使用原摘要")
            summary = generator.use_original_abstract(paper)
        
        # 3) 保存摘要
        summary_path = paper_output_dir / "detailed_summary.md"
        generator.save_summary(summary, summary_path, metadata=paper)
        
        high_rel_summaries.append({
            'arxiv_id': arxiv_id,
            'title': paper['title'],
            'score': score,
            'summary': summary,
            'has_full_md': md_path is not None
        })
    

    
    # ===== 第 5 步: 处理低相关度论文 =====
    logger.info("═" * 70)
    logger.info("第 5 步: 处理低相关度论文（使用原摘要）")
    logger.info("═" * 70)
    
    low_rel_summaries = []
    for paper, score in low_rel:
        arxiv_id = paper.get('arxiv_id', paper.get('id'))
        summary = generator.use_original_abstract(paper)
        
        low_rel_summaries.append({
            'arxiv_id': arxiv_id,
            'title': paper['title'],
            'score': score,
            'summary': summary
        })
    
    logger.info(f"✅ 已处理 {len(low_rel_summaries)} 篇低相关度论文")
    
    # 保存低相关度摘要到 JSON，供评审报告使用
    low_rel_json_path = paper_dir / "low_relevance_summaries.json"
    with open(low_rel_json_path, 'w', encoding='utf-8') as f:
        json.dump(low_rel_summaries, f, ensure_ascii=False, indent=2, default=str)
    logger.info(f"✅ 低相关度摘要已保存: {low_rel_json_path}")
    
    # ===== 第 6 步: 生成综合报告 =====
    logger.info("═" * 70)
    logger.info("第 6 步: 生成综合报告")
    logger.info("═" * 70)
    
    report_path = paper_dir / "summary_report.md"
    generate_summary_report(
        source_metadata,
        high_rel_summaries,
        low_rel_summaries,
        report_path
    )
    
    logger.info(f"✅ 综合报告已保存: {report_path}")

    logger.info("═" * 70)
    logger.info(f"✅ 完成！所有结果已保存到: {paper_dir.resolve()}")
    logger.info("═" * 70)


def generate_summary_report(
    source_metadata: dict,
    high_rel_summaries: list,
    low_rel_summaries: list,
    output_path: Path
):
    """生成综合报告"""
    
    content = f"""# 文献综述综合报告

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 源论文信息

- **标题**: {source_metadata['title']}
- **作者**: {', '.join(source_metadata.get('authors', [])[:5])}
- **摘要**: {source_metadata.get('abstract', '无摘要')[:200]}...

---

## 高相关度文献 ({len(high_rel_summaries)} 篇)

"""
    
    for i, item in enumerate(high_rel_summaries, 1):
        content += f"""### {i}. {item['title']}

**相关度**: {item['score']:.3f} | **arXiv ID**: {item['arxiv_id']} | **完整MD**: {'✅' if item['has_full_md'] else '❌'}

{item['summary']}

---

"""
    
    content += f"""## 低相关度文献 ({len(low_rel_summaries)} 篇)

<details>
<summary>点击展开查看</summary>

"""
    
    for i, item in enumerate(low_rel_summaries, 1):
        content += f"""### {i}. {item['title']}

**相关度**: {item['score']:.3f} | **arXiv ID**: {item['arxiv_id']}

{item['summary'][:300]}...

---

"""
    
    content += """
</details>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='相关度打分和摘要生成流水线'
    )
    
    parser.add_argument(
        'paper_id',
        help='论文ID（例如：2401.12345）'
    )
    
    parser.add_argument(
        '-k', '--top-k',
        type=int,
        default=15,
        help='高相关度论文数量（默认: 15）'
    )
    
    parser.add_argument(
        '-l', '--language',
        choices=['chinese', 'english'],
        default='chinese',
        help='摘要语言（默认: chinese）'
    )
    
    parser.add_argument(
        '-i', '--input-dir',
        default=None,
        help='输入目录（默认: pipeline/literature_search_results）'
    )
    
    args = parser.parse_args()
    
    run_ranking_and_summary(
        paper_id=args.paper_id,
        top_k=args.top_k,
        language=args.language,
        input_dir=args.input_dir
    )


if __name__ == '__main__':
    main()
