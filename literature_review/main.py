#!/usr/bin/env python3
"""
文献综述流水线 - 主程序
自动解析论文、生成搜索查询、检索相关文献
"""
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import logging

# 导入模块
from pdf_parser_mineru import parse_pdf_to_markdown
from metadata_extractor import extract_metadata, validate_metadata
from query_generator import generate_queries_from_metadata
from arxiv_searcher import search_and_deduplicate
from literature_review.logger import get_logger


def  main():
    parser = argparse.ArgumentParser(
        description='文献综述流水线 - 自动解析论文并检索相关文献'
    )
    parser.add_argument(
        'pdf_path',
        help='PDF 论文路径'
    )
    parser.add_argument(
        '-o', '--output-dir',
        help='输出目录（默认：与PDF同目录）',
        default=None
    )
    parser.add_argument(
        '-n', '--num-queries',
        type=int,
        help='生成的搜索查询数量（默认：7）',
        default=7
    )
    parser.add_argument(
        '-r', '--results-per-query',
        type=int,
        help='每个查询返回的最大结果数（默认：10）',
        default=10
    )
    parser.add_argument(
        '-y', '--start-year',
        type=int,
        help='论文起始年份（默认：2020）',
        default=2020
    )
    parser.add_argument(
        '--skip-search',
        action='store_true',
        help='跳过 arXiv 搜索，仅解析论文'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'csv', 'both'],
        default='both',
        help='输出格式（默认：both）'
    )
    
    args = parser.parse_args()

    # 获取日志器
    logger = get_logger("main")

    # 验证 PDF 文件
    if not os.path.exists(args.pdf_path):
        logger.error(f"❌ 错误: PDF 文件不存在: {args.pdf_path}")
        sys.exit(1)
    
    # 设置输出目录
    if args.output_dir is None:
        args.output_dir = os.path.dirname(args.pdf_path) or '.'
    
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 70)
    logger.info("📚 文献综述流水线")
    logger.info("=" * 70)
    logger.info(f"PDF 文件: {args.pdf_path}")
    logger.info(f"输出目录: {args.output_dir}")
    logger.info(f"查询数量: {args.num_queries}")
    logger.info(f"起始年份: {args.start_year}")
    logger.info("=" * 70)
    
    # 步骤 1: 解析 PDF
    logger.info("\n" + "=" * 70)
    logger.info("第 1 步: 解析 PDF")
    logger.info("=" * 70)

    try:
        parse_result = parse_pdf_to_markdown(args.pdf_path, args.output_dir)
        markdown_text = parse_result['markdown']
        logger.info(f"✅ PDF 解析成功！")
    except Exception as e:
        logger.exception(f"❌ PDF 解析失败: {e}")
        sys.exit(1)
    
    # 步骤 2: 提取元数据
    logger.info("\n" + "=" * 70)
    logger.info("第 2 步: 提取元数据")
    logger.info("=" * 70)

    try:
        metadata = extract_metadata(markdown_text)

        # 保存元数据
        metadata_path = output_path / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        logger.info(f"✅ 元数据已保存: {metadata_path}")

        # 检查验证结果
        if not metadata['validation']['is_valid']:
            logger.warning(f"⚠️  警告: 元数据不完整，缺少: {', '.join(metadata['validation']['missing_fields'])}")
            logger.warning("继续执行，但搜索结果可能不准确")

    except Exception as e:
        logger.exception(f"❌ 元数据提取失败: {e}")
        sys.exit(1)
    
    # 步骤 3: 生成搜索查询
    logger.info("\n" + "=" * 70)
    logger.info("第 3 步: 生成搜索查询")
    logger.info("=" * 70)

    try:
        queries = generate_queries_from_metadata(metadata, num_queries=args.num_queries)

        # 保存查询
        queries_path = output_path / "search_queries.json"
        with open(queries_path, 'w', encoding='utf-8') as f:
            json.dump(queries, f, ensure_ascii=False, indent=2)

        logger.info(f"✅ 查询已保存: {queries_path}")

    except Exception as e:
        logger.exception(f"❌ 查询生成失败: {e}")
        sys.exit(1)
    
    # 步骤 4: 搜索 arXiv
    if not args.skip_search:
        logger.info("\n" + "=" * 70)
        logger.info("第 4 步: 搜索 arXiv")
        logger.info("=" * 70)

        try:
            papers = search_and_deduplicate(
                queries,
                max_results_per_query=args.results_per_query,
                start_year=args.start_year
            )

            # 步骤 5: 导出结果
            logger.info("\n" + "=" * 70)
            logger.info("第 5 步: 导出结果")
            logger.info("=" * 70)
            
            # JSON 格式
            if args.format in ['json', 'both']:
                results_json_path = output_path / "related_papers.json"
                with open(results_json_path, 'w', encoding='utf-8') as f:
                    json.dump(papers, f, ensure_ascii=False, indent=2)
                logger.info(f"✅ JSON 结果已保存: {results_json_path}")
            
            # CSV 格式
            if args.format in ['csv', 'both']:
                import csv
                results_csv_path = output_path / "related_papers.csv"
                with open(results_csv_path, 'w', newline='', encoding='utf-8') as f:
                    if papers:
                        fieldnames = ['id', 'title', 'authors', 'published', 'categories', 'arxiv_url', 'source_query']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        for paper in papers:
                            writer.writerow({
                                'id': paper['id'],
                                'title': paper['title'],
                                'authors': '; '.join(paper['authors']),
                                'published': paper['published'],
                                'categories': '; '.join(paper['categories']),
                                'arxiv_url': paper['arxiv_url'],
                                'source_query': paper.get('source_query', '')
                            })
                logger.info(f"✅ CSV 结果已保存: {results_csv_path}")
            
            # 生成摘要报告
            logger.info("\n" + "=" * 70)
            logger.info("📊 处理摘要")
            logger.info("=" * 70)
            logger.info(f"论文标题: {metadata.get('title', '未知')}")
            logger.info(f"作者数量: {len(metadata.get('authors', []))}")
            logger.info(f"章节数量: {len(metadata.get('sections', []))}")
            logger.info(f"生成查询: {len(queries)} 条")
            logger.info(f"找到相关论文: {len(papers)} 篇")

            if papers:
                # 按年份统计
                year_stats = {}
                for paper in papers:
                    year = paper['published'][:4]
                    year_stats[year] = year_stats.get(year, 0) + 1

                logger.info(f"\n按年份分布:")
                for year in sorted(year_stats.keys(), reverse=True):
                    logger.info(f"  {year}: {year_stats[year]} 篇")
        
        except Exception as e:
            logger.exception(f"❌ arXiv 搜索失败: {e}")
            sys.exit(1)
    else:
        logger.warning("\n⏭️  跳过 arXiv 搜索（--skip-search）")
    
    logger.info("\n" + "=" * 70)
    logger.info("✅ 流水线执行完成！")
    logger.info("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger = get_logger("main")
        logger.warning("\n\n⚠️  用户中断")
        sys.exit(130)
    except Exception as e:
        logger = get_logger("main")
        logger.exception(f"\n\n❌ 未预期的错误: {e}")
        sys.exit(1)
