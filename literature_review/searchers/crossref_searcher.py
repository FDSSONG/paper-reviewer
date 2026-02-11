#!/usr/bin/env python3
"""
CrossRef 搜索模块
继承自 BaseSearcher，使用 CrossRef API 搜索相关论文
"""
import time
import urllib.parse
import urllib.request
import json
from typing import List, Dict, Any

from literature_review.searchers.base_searcher import BaseSearcher


class CrossRefSearcher(BaseSearcher):
    """CrossRef 搜索器类（继承自 BaseSearcher）"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化 CrossRef 搜索器

        Args:
            config: 配置字典，包含 max_retries, delay, timeout 等参数
        """
        super().__init__(config)
        self.base_url = "https://api.crossref.org/works"
        self.email = config.get('email', None)  # 用于 User-Agent
        self.logger.info("CrossRef 搜索器初始化完成")

    def search(
        self,
        query: str,
        max_results: int = 20,
        since_year: int = 2020
    ) -> List[Dict[str, Any]]:
        """
        在 CrossRef 上搜索论文（带指数退避重试）

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
            'rows': max_results,
            'filter': f'from-pub-date:{since_year}',
            'sort': 'relevance',
            'order': 'desc'
        }

        url = f"{self.base_url}?{urllib.parse.urlencode(params)}"

        # 构建请求头（CrossRef 推荐在 User-Agent 中包含邮箱）
        headers = {
            'User-Agent': f'LiteratureReview/1.0 ({self.email or "no-email"})'
        }

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                # 发送请求
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    data = json.loads(response.read().decode('utf-8'))

                papers = []
                for item in data.get('message', {}).get('items', []):
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
                    self.logger.warning(f"CrossRef 请求失败: {e}")
                    self.logger.info(f"第 {attempt + 1} 次重试，等待 {wait:.0f}s...")
                    time.sleep(wait)
                else:
                    self.logger.exception(f"CrossRef 搜索失败: {e}")
                    return []

        self.logger.exception(f"CrossRef 搜索失败（已重试 {self.max_retries} 次）: {last_error}")
        return []

    def _parse_paper(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析 CrossRef API 返回的论文数据

        Args:
            item: API 返回的单篇论文数据

        Returns:
            解析后的论文数据
        """
        try:
            # 提取作者
            authors = []
            for author in item.get('author', []):
                given = author.get('given', '')
                family = author.get('family', '')
                if given and family:
                    authors.append(f"{given} {family}")
                elif family:
                    authors.append(family)

            # 提取标题
            title_list = item.get('title', [])
            title = title_list[0] if title_list else ''

            # 提取发表日期
            published_date = ''
            if 'published' in item:
                date_parts = item['published'].get('date-parts', [[]])[0]
                if len(date_parts) >= 1:
                    year = date_parts[0]
                    month = date_parts[1] if len(date_parts) >= 2 else 1
                    day = date_parts[2] if len(date_parts) >= 3 else 1
                    published_date = f"{year:04d}-{month:02d}-{day:02d}"

            # 构建论文数据
            paper = {
                'doi': item.get('DOI', ''),
                'title': title.strip(),
                'authors': authors,
                'abstract': item.get('abstract', '').strip() if item.get('abstract') else '',
                'published': published_date,
                'venue': item.get('container-title', [''])[0] if item.get('container-title') else '',
                'type': item.get('type', ''),
                'doi_url': f"https://doi.org/{item.get('DOI', '')}" if item.get('DOI') else ''
            }

            return paper
        except Exception as e:
            self.logger.warning(f"解析论文数据失败: {e}")
            return None

    def normalize_paper(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化论文格式（CrossRef → 通用格式）

        Args:
            paper: CrossRef 原始格式的论文数据

        Returns:
            标准化后的论文数据
        """
        # 保留 CrossRef 原始字段，同时添加标准字段
        normalized = paper.copy()
        normalized.update({
            'id': paper['doi'],
            'url': paper['doi_url'],
            'source': 'crossref'
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


