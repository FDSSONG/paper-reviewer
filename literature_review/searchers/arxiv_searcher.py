#!/usr/bin/env python3
"""
ArXiv 搜索模块 - 重构版本
继承自 BaseSearcher，使用 arXiv API 搜索相关论文
"""
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import List, Dict, Any

from literature_review.searchers.base_searcher import BaseSearcher


class ArxivSearcher(BaseSearcher):
    """ArXiv 搜索器类（继承自 BaseSearcher）"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化 arXiv 搜索器

        Args:
            config: 配置字典，包含 max_retries, delay, timeout 等参数
        """
        super().__init__(config)
        self.logger.info("ArXiv 搜索器初始化完成")

    def search(
        self,
        query: str,
        max_results: int = 20,
        since_year: int = 2020
    ) -> List[Dict[str, Any]]:
        """
        在 arXiv 上搜索论文（带指数退避重试）

        Args:
            query: 搜索查询字符串
            max_results: 最大返回结果数
            since_year: 起始年份（默认2020）

        Returns:
            标准化的论文列表
        """
        # 构建搜索 URL
        base_url = "http://export.arxiv.org/api/query?"

        # arXiv API 参数
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }

        url = base_url + urllib.parse.urlencode(params)

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                # 发送请求
                with urllib.request.urlopen(url, timeout=self.timeout) as response:
                    xml_data = response.read()

                # 解析 XML
                root = ET.fromstring(xml_data)

                # 命名空间
                ns = {
                    'atom': 'http://www.w3.org/2005/Atom',
                    'arxiv': 'http://arxiv.org/schemas/atom'
                }

                papers = []

                for entry in root.findall('atom:entry', ns):
                    # 提取基本信息
                    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')

                    # 提取作者
                    authors = []
                    for author in entry.findall('atom:author', ns):
                        name = author.find('atom:name', ns).text
                        authors.append(name)

                    # 摘要
                    abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')

                    # 发布和更新日期
                    published = entry.find('atom:published', ns).text
                    updated = entry.find('atom:updated', ns).text

                    # 提取年份进行过滤
                    pub_year = int(published[:4])
                    if pub_year < since_year:
                        continue

                    # ID（从链接中提取）
                    arxiv_id = entry.find('atom:id', ns).text.split('/abs/')[-1]

                    # 分类
                    categories = []
                    for category in entry.findall('atom:category', ns):
                        categories.append(category.get('term'))

                    # 构建论文数据（arXiv 原始格式）
                    paper = {
                        'arxiv_id': arxiv_id,
                        'title': title,
                        'authors': authors,
                        'abstract': abstract,
                        'published': published[:10],  # YYYY-MM-DD
                        'updated': updated[:10],
                        'categories': categories,
                        'pdf_url': f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                        'arxiv_url': f"https://arxiv.org/abs/{arxiv_id}"
                    }

                    # 标准化格式
                    normalized_paper = self.normalize_paper(paper)
                    papers.append(normalized_paper)

                return papers

            except Exception as e:
                last_error = e
                error_str = str(e)
                # 判断是否为可重试的错误
                retryable = any(keyword in error_str for keyword in [
                    '429', '503', 'IncompleteRead', 'Connection',
                    'Too Many Requests', 'Service Unavailable',
                    'RemoteDisconnected', 'ConnectionReset', 'SSL', 'EOF',
                    'timed out', 'timeout'
                ])

                if retryable and attempt < self.max_retries:
                    wait = self.delay * (2 ** attempt)  # 指数退避
                    self.logger.warning(f"arXiv 请求失败: {e}")
                    self.logger.info(f"第 {attempt + 1} 次重试，等待 {wait:.0f}s...")
                    time.sleep(wait)
                else:
                    self.logger.exception(f"arXiv 搜索失败: {e}")
                    return []

        self.logger.exception(f"arXiv 搜索失败（已重试 {self.max_retries} 次）: {last_error}")
        return []

    def batch_search(
        self,
        queries: List[str],
        max_results_per_query: int = 10,
        since_year: int = 2020
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        批量搜索多个查询

        Args:
            queries: 查询列表
            max_results_per_query: 每个查询的最大结果数
            since_year: 起始年份

        Returns:
            字典，键为查询字符串，值为论文列表
        """
        self.logger.info(f"🔎 开始批量搜索 {len(queries)} 个查询...")

        results = {}

        for i, query in enumerate(queries, 1):
            # 如果query是字典，提取query字符串
            if isinstance(query, dict):
                query_str = query.get('query', str(query))
                perspective = query.get('perspective', 'unknown')
            else:
                query_str = str(query)
                perspective = 'unknown'

            self.logger.info(f"[{i}/{len(queries)}] 搜索: {query_str}")
            if perspective != 'unknown':
                self.logger.info(f"视角: {perspective}")

            papers = self.search(
                query=query_str,
                max_results=max_results_per_query,
                since_year=since_year
            )

            results[query_str] = papers
            self.logger.info(f"找到 {len(papers)} 篇论文")

            # 延迟以避免触发速率限制
            if i < len(queries):
                time.sleep(self.delay)

        return results

    def normalize_paper(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化论文格式（arXiv → 通用格式）

        Args:
            paper: arXiv 原始格式的论文数据

        Returns:
            标准化后的论文数据
        """
        # 保留 arXiv 原始字段，同时添加标准字段
        normalized = paper.copy()
        normalized.update({
            'id': paper['arxiv_id'],
            'url': paper['arxiv_url'],
            'source': 'arxiv'
        })
        return normalized

    def deduplicate(self, results: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        去重论文结果

        Args:
            results: 批量搜索的结果

        Returns:
            去重后的论文列表
        """
        seen_ids = set()
        unique_papers = []

        for query, papers in results.items():
            for paper in papers:
                paper_id = paper.get('id') or paper.get('arxiv_id')
                if paper_id not in seen_ids:
                    seen_ids.add(paper_id)
                    # 添加来源查询信息
                    paper['source_query'] = query
                    unique_papers.append(paper)

        return unique_papers

    def search_and_deduplicate(
        self,
        queries: List[str],
        max_results_per_query: int = 10,
        since_year: int = 2020
    ) -> List[Dict[str, Any]]:
        """
        搜索并去重（一站式函数）

        Args:
            queries: 查询列表
            max_results_per_query: 每个查询的最大结果数
            since_year: 起始年份

        Returns:
            去重后的论文列表
        """
        results = self.batch_search(queries, max_results_per_query, since_year)
        unique_papers = self.deduplicate(results)

        self.logger.info(
            f"✅ 搜索完成！总查询数: {len(queries)}, "
            f"去重前: {sum(len(papers) for papers in results.values())} 篇, "
            f"去重后: {len(unique_papers)} 篇"
        )

        return unique_papers
