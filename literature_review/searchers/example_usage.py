"""
搜索引擎工厂使用示例
"""
from literature_review.searchers import create_searcher, create_multi_searchers
from literature_review.logger import get_logger

logger = get_logger("example")


def example_single_searcher():
    """示例：使用单个搜索引擎"""
    logger.info("=" * 50)
    logger.info("示例 1: 使用单个搜索引擎（从配置文件读取）")
    logger.info("=" * 50)

    # 创建搜索引擎（自动从配置文件读取选择的引擎）
    searcher = create_searcher()

    # 搜索论文
    papers = searcher.search(
        query="machine learning",
        max_results=5,
        since_year=2023
    )

    logger.info(f"找到 {len(papers)} 篇论文")
    for i, paper in enumerate(papers, 1):
        logger.info(f"{i}. {paper['title']}")


def example_specific_searcher():
    """示例：指定特定搜索引擎"""
    logger.info("=" * 50)
    logger.info("示例 2: 指定使用 arXiv 搜索引擎")
    logger.info("=" * 50)

    # 明确指定使用 arXiv
    searcher = create_searcher(engine_name="arxiv")

    # 批量搜索
    queries = ["deep learning", "neural networks"]
    results = searcher.batch_search(queries, max_results_per_query=3)

    for query, papers in results.items():
        logger.info(f"查询 '{query}': {len(papers)} 篇论文")


def example_multi_searchers():
    """示例：使用多个搜索引擎（需要在配置文件中启用）"""
    logger.info("=" * 50)
    logger.info("示例 3: 使用多个搜索引擎")
    logger.info("=" * 50)

    # 创建多个搜索引擎
    searchers = create_multi_searchers()

    logger.info(f"创建了 {len(searchers)} 个搜索引擎")

    # 使用每个搜索引擎搜索
    query = "transformer architecture"
    for searcher in searchers:
        papers = searcher.search(query, max_results=3)
        logger.info(f"{searcher.__class__.__name__}: {len(papers)} 篇论文")


if __name__ == "__main__":
    # 运行示例
    example_single_searcher()
    example_specific_searcher()
    example_multi_searchers()
