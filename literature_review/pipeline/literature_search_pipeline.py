"""
文献检索流水线 - 自动生成搜索查询并获取相关论文

工作流程：
1. 读取 mineru_pipeline 生成的 full.md 文件
2. 提取论文元数据（标题、摘要、关键内容）
3. 使用 DeepSeek AI 生成 5-10 条英文检索句
4. 在 arXiv 搜索 2020 年后的相关论文
5. 批量保存元数据到本地
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime
from literature_review.logger import get_logger

logger = get_logger("literature_search_pipeline")

# 导入已有的模块
sys.path.append(str(Path(__file__).parent.parent))
from literature_review.metadata_extractor import MetadataExtractor
from literature_review.query_generator import QueryGenerator
from literature_review.arxiv_searcher import ArxivSearcher


def load_markdown_from_mineru(paper_id: str, base_dir: Path = None) -> str:
    """
    从 mineru_pipeline 输出目录加载 full.md
    
    Args:
        paper_id: 论文ID（例如 '2401.12345'）
        base_dir: mineru_pipeline 输出根目录，默认为 'pipeline/outputs'
    
    Returns:
        Markdown 文本内容
    """
    if base_dir is None:
        base_dir = Path(__file__).parent / "outputs"
    
    md_path = base_dir / paper_id / "full.md"
    
    if not md_path.exists():
        raise FileNotFoundError(
            f"未找到 Markdown 文件: {md_path}\n"
            f"请先运行 pipeline/mineru_pipeline.py 生成 MD 文件"
        )
    
    with open(md_path, 'r', encoding='utf-8') as f:
        return f.read()


def run_literature_search(
    paper_id: str,
    num_queries: int = 7,
    since_year: int = 2020,
    max_results_per_query: int = 20,
    output_dir: str = None
):
    """
    运行完整的文献检索流水线
    
    Args:
        paper_id: 论文ID
        num_queries: 生成的查询数量
        since_year: 起始年份
        max_results_per_query: 每个查询的最大结果数
        output_dir: 输出目录（默认为 pipeline/literature_search_results）
    """
    # 如果没有指定输出目录，使用 pipeline 下的默认目录
    if output_dir is None:
        output_dir = str(Path(__file__).parent / "literature_search_results")
    logger.info("═" * 70)
    logger.info("📚 文献检索自动化流水线")
    logger.info("═" * 70)
    logger.info(f"论文 ID: {paper_id} | 查询数量: {num_queries} | 起始年份: {since_year} | 输出目录: {output_dir}")
    
    output_path = Path(output_dir) / paper_id
    output_path.mkdir(parents=True, exist_ok=True)
    
    # ===== 第 1 步: 加载 Markdown =====
    logger.info("═" * 70)
    logger.info("第 1 步: 加载 Markdown 文件")
    logger.info("═" * 70)
    
    try:
        markdown_text = load_markdown_from_mineru(paper_id)
        logger.info(f"✅ 成功加载 Markdown ({len(markdown_text)} 字符)")
        
        # 保存副本
        md_copy_path = output_path / f"{paper_id}_source.md"
        try:
            md_copy_path.write_text(markdown_text, encoding='utf-8')
            logger.info(f"   已保存副本: {md_copy_path}")
        except Exception as e:
            logger.error(f"错误: 无法保存 Markdown 副本到 {md_copy_path}: {e}")
            return # If we can't save the source, something is wrong, exit.
    except FileNotFoundError as e:
        logger.error(f"❌ 错误: {e}")
        return
    

    
    # ===== 第 2 步: 提取元数据 =====
    logger.info("═" * 70)
    logger.info("第 2 步: 提取论文元数据")
    logger.info("═" * 70)
    
    extractor = MetadataExtractor()
    
    # 优先从 MinerU 的结构化 JSON 提取标题和作者（更准确）
    content_list_path = Path(__file__).parent / "outputs" / paper_id / "meta" / "content_list_v2.json"
    content_list_meta = extractor.extract_from_content_list(str(content_list_path))
    
    # 从 Markdown 提取完整元数据（摘要、章节等）
    metadata = extractor.extract_metadata(markdown_text)
    
    # 用 content_list 的结果覆盖 regex 提取的 title/authors（如果有）
    if content_list_meta.get('title'):
        metadata['title'] = content_list_meta['title']
        logger.info("标题来源: content_list_v2.json (结构化)")
    if content_list_meta.get('authors'):
        metadata['authors'] = content_list_meta['authors']
        logger.info("作者来源: content_list_v2.json (结构化)")
    
    logger.info(f"标题: {metadata['title']}")
    authors_str = ', '.join(metadata['authors'][:3]) if metadata['authors'] else '未找到'
    logger.info(f"作者: {authors_str}...")
    logger.info(f"章节数: {len(metadata['sections'])}")
    abstract_len = len(metadata.get('abstract', ''))
    logger.info(f"摘要长度: {abstract_len} 字符")
    
    # 保存元数据
    metadata_path = output_path / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    logger.info(f"   已保存: {metadata_path}")
    

    
    # ===== 第 3 步: 生成搜索查询 =====
    logger.info("═" * 70)
    logger.info("第 3 步: 使用 DeepSeek AI 生成搜索查询")
    logger.info("═" * 70)
    
    generator = QueryGenerator()
    queries = generator.generate_queries(
        markdown_text=markdown_text,
        metadata=metadata,
        num_queries=num_queries
    )
    
    logger.info(f"✅ 生成了 {len(queries)} 条查询:")
    for i, query in enumerate(queries, 1):
        logger.info(f"  {i}. {query}")
    
    # 保存查询
    queries_path = output_path / "search_queries.json"
    with open(queries_path, 'w', encoding='utf-8') as f:
        json.dump(queries, f, ensure_ascii=False, indent=2)
    logger.info(f"已保存: {queries_path}")
    

    
    # ===== 第 4 步: 搜索 arXiv =====
    logger.info("═" * 70)
    logger.info("第 4 步: 搜索 arXiv (2020年后)")
    logger.info("═" * 70)
    
    searcher = ArxivSearcher()
    
    all_results = []
    seen_ids = set()
    
    for i, query in enumerate(queries, 1):
        logger.info(f"搜索 {i}/{len(queries)}: {query[:60]}...")
        
        results = searcher.search(
            query=query,
            max_results=max_results_per_query,
            since_year=since_year
        )
        
        # 去重
        new_results = []
        for result in results:
            if result['arxiv_id'] not in seen_ids:
                seen_ids.add(result['arxiv_id'])
                new_results.append(result)
        
        logger.info(f"找到 {len(results)} 篇论文，去重后 {len(new_results)} 篇")
        all_results.extend(new_results)
        
        # 查询间延迟，避免触发 arXiv 速率限制
        if i < len(queries):
            time.sleep(searcher.delay)
    
    logger.info(f"✅ 总计找到 {len(all_results)} 篇相关论文（去重后）")
    
    # ===== 第 5 步: 保存结果 =====
    logger.info("═" * 70)
    logger.info("第 5 步: 保存结果")
    logger.info("═" * 70)
    
    # 保存 JSON
    results_json_path = output_path / "arxiv_results.json"
    with open(results_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    logger.info(f"✅ JSON 格式: {results_json_path}")
    
    # 保存 CSV
    results_csv_path = output_path / "arxiv_results.csv"
    searcher.save_to_csv(all_results, results_csv_path)
    logger.info(f"✅ CSV 格式: {results_csv_path}")
    
    # 生成摘要报告
    summary_path = output_path / "search_summary.txt"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("文献检索摘要报告\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"论文 ID: {paper_id}\n")
        f.write(f"检索时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"查询数量: {len(queries)}\n")
        f.write(f"起始年份: {since_year}\n")
        f.write(f"找到论文: {len(all_results)} 篇\n\n")
        
        f.write("=" * 70 + "\n")
        f.write("搜索查询列表\n")
        f.write("=" * 70 + "\n\n")
        for i, query in enumerate(queries, 1):
            f.write(f"{i}. {query}\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("前 10 篇相关论文\n")
        f.write("=" * 70 + "\n\n")
        for i, paper in enumerate(all_results[:10], 1):
            f.write(f"{i}. {paper['title']}\n")
            f.write(f"   作者: {', '.join(paper['authors'][:3])}\n")
            f.write(f"   年份: {paper['published'][:4]}\n")
            f.write(f"   链接: {paper['pdf_url']}\n\n")
    
    logger.info(f"✅ 摘要报告: {summary_path}")
    
    logger.info("═" * 70)
    logger.info(f"✅ 完成！所有结果已保存到: {output_path.resolve()}")
    logger.info("═" * 70)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='文献检索自动化流水线 - 从 mineru_pipeline 输出开始'
    )
    
    parser.add_argument(
        'paper_id',
        help='论文ID（例如：2401.12345）'
    )
    
    parser.add_argument(
        '-n', '--num-queries',
        type=int,
        default=7,
        help='生成的查询数量（默认: 7）'
    )
    
    parser.add_argument(
        '-y', '--since-year',
        type=int,
        default=2020,
        help='起始年份（默认: 2020）'
    )
    
    parser.add_argument(
        '-r', '--max-results',
        type=int,
        default=20,
        help='每个查询的最大结果数（默认: 20）'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        default=None,
        help='输出目录（默认: pipeline/literature_search_results）'
    )
    
    args = parser.parse_args()
    
    run_literature_search(
        paper_id=args.paper_id,
        num_queries=args.num_queries,
        since_year=args.since_year,
        max_results_per_query=args.max_results,
        output_dir=args.output_dir
    )


if __name__ == '__main__':
    main()
