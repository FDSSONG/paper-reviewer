#!/usr/bin/env python3
"""
Semantic Scholar 搜索模块
继承自 BaseSearcher，使用 Semantic Scholar API 搜索相关论文
"""
import time
import urllib.parse
import urllib.request
import json
from typing import List, Dict, Any

from literature_review.searchers.base_searcher import BaseSearcher


class SemanticScholarSearcher(BaseSearcher):
    """Semantic Scholar 搜索器类（继承自 BaseSearcher）"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化 Semantic Scholar 搜索器

        Args:
            config: 配置字典，包含 max_retries, delay, timeout 等参数
        """
        super().__init__(config)
        self.base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        self.api_key = config.get('api_key', None)  # API key 是可选的
        self.logger.info("Semantic Scholar 搜索器初始化完成")

    def search(
        self,
        query: str,
        max_results: int = 20,
        since_year: int = 2020
    ) -> List[Dict[str, Any]]:
        """
        在 Semantic Scholar 上搜索论文（带指数退避重试）

        Args:
            query: 搜索查询字符串
            max_results: 最大返回结果数
            since_year: 起始年份（默认2020）

        Returns:
            标准化的论文列表
        """
        # 构建查询参数
        params = {
            'query': query,
            'limit': max_results,
            'fields': 'paperId,title,authors,year,abstract,url,venue,publicationDate,citationCount',
            'year': f'{since_year}-'  # 从 since_year 到现在
        }

        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"

        # 构建请求头
        headers = {}
        if self.api_key:
            headers['x-api-key'] = self.api_key

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                # 发送请求
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    data = json.loads(response.read().decode('utf-8'))

                papers = []
                for item in data.get('data', []):
                    # 提取论文信息
                    paper = self._parse_paper(item)
                    if paper:
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
                    self.logger.warning(f"Semantic Scholar 请求失败: {e}")
                    self.logger.info(f"第 {attempt + 1} 次重试，等待 {wait:.0f}s...")
                    time.sleep(wait)
                else:
                    self.logger.exception(f"Semantic Scholar 搜索失败: {e}")
                    return []

        self.logger.exception(f"Semantic Scholar 搜索失败（已重试 {self.max_retries} 次）: {last_error}")
        return []

    def _parse_paper(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析 Semantic Scholar API 返回的论文数据

        Args:
            item: API 返回的单篇论文数据

        Returns:
            解析后的论文数据
        """
        try:
            # 提取作者
            authors = []
            for author in item.get('authors', []):
                if 'name' in author:
                    authors.append(author['name'])

            # 构建论文数据
            paper = {
                's2_id': item.get('paperId', ''),
                'title': item.get('title', '').strip(),
                'authors': authors,
                'abstract': item.get('abstract', '').strip() if item.get('abstract') else '',
                'year': item.get('year'),
                'published': item.get('publicationDate', ''),
                'venue': item.get('venue', ''),
                'citation_count': item.get('citationCount', 0),
                's2_url': item.get('url', '')
            }

            return paper
        except Exception as e:
            self.logger.warning(f"解析论文数据失败: {e}")
            return None

    def normalize_paper(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化论文格式（Semantic Scholar → 通用格式）

        Args:
            paper: Semantic Scholar 原始格式的论文数据

        Returns:
            标准化后的论文数据
        """
        # 保留 Semantic Scholar 原始字段，同时添加标准字段
        normalized = paper.copy()
        normalized.update({
            'id': paper['s2_id'],
            'url': paper['s2_url'],
            'source': 'semantic_scholar'
        })
        return normalized

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

