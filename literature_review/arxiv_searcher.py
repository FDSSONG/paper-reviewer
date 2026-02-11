#!/usr/bin/env python3
"""
ArXiv 搜索模块 - 类封装版本
使用 arXiv API 搜索相关论文并批量获取元数据
"""
import time
import csv
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from literature_review.logger import get_logger

logger = get_logger("arxiv_searcher")


class ArxivSearcher:
    """ArXiv 搜索器类"""
    
    def __init__(self, delay: float = 5.0, max_retries: int = 3):
        """
        初始化搜索器1
        
        Args:
            delay: 查询之间的延迟（秒），避免触发速率限制
            max_retries: 请求失败时的最大重试次数
        """
        self.delay = delay
        self.max_retries = max_retries
    
    def search(
        self,
        query: str,
        max_results: int = 20,
        since_year: int = 2020,
        sort_by: str = "relevance"
    ) -> List[Dict]:
        """
        在 arXiv 上搜索论文（带指数退避重试）
        
        Args:
            query: 搜索查询字符串
            max_results: 最大返回结果数
            since_year: 起始年份（默认2020）
            sort_by: 排序方式 "relevance" 或 "lastUpdatedDate"
        
        Returns:
            [
                {
                    "arxiv_id": "2301.12345",
                    "title": "Paper Title",
                    "authors": ["Author 1", "Author 2"],
                    "abstract": "Abstract text...",
                    "published": "2023-01-15",
                    "updated": "2023-01-20",
                    "categories": ["cs.AI", "cs.LG"],
                    "pdf_url": "https://arxiv.org/pdf/2301.12345",
                    "arxiv_url": "https://arxiv.org/abs/2301.12345"
                },
                ...
            ]
        """
        # 构建搜索 URL
        base_url = "http://export.arxiv.org/api/query?"
        
        # arXiv API 参数
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': sort_by,
            'sortOrder': 'descending'
        }
        
        url = base_url + urllib.parse.urlencode(params)
        
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                # 发送请求
                with urllib.request.urlopen(url, timeout=30) as response:
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
                    
                    # PDF链接
                    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                    
                    paper = {
                        'arxiv_id': arxiv_id,
                        'title': title,
                        'authors': authors,
                        'abstract': abstract,
                        'published': published[:10],  # YYYY-MM-DD
                        'updated': updated[:10],
                        'categories': categories,
                        'pdf_url': pdf_url,
                        'arxiv_url': f"https://arxiv.org/abs/{arxiv_id}"
                    }
                    
                    papers.append(paper)
                
                return papers
            
            except Exception as e:
                last_error = e
                error_str = str(e)
                # 判断是否为可重试的错误 (429/503/IncompleteRead/连接问题)
                retryable = any(keyword in error_str for keyword in [
                    '429', '503', 'IncompleteRead', 'Connection',
                    'Too Many Requests', 'Service Unavailable',
                    'RemoteDisconnected', 'ConnectionReset', 'SSL', 'EOF',
                    'timed out', 'timeout'
                ])

                if retryable and attempt < self.max_retries:
                    wait = self.delay * (2 ** attempt)  # 指数退避: 5s, 10s, 20s
                    logger.warning(f"arXiv 请求失败: {e}")
                    logger.info(f"第 {attempt + 1} 次重试，等待 {wait:.0f}s...")
                    time.sleep(wait)
                else:
                    logger.exception(f"arXiv 搜索失败: {e}")
                    return []

        logger.exception(f"arXiv 搜索失败（已重试 {self.max_retries} 次）: {last_error}")
        return []
    
    def batch_search(
        self,
        queries: List[str],
        max_results_per_query: int = 10,
        since_year: int = 2020
    ) -> Dict[str, List[Dict]]:
        """
        批量搜索多个查询
        
        Args:
            queries: 查询列表
            max_results_per_query: 每个查询的最大结果数
            since_year: 起始年份
        
        Returns:
            {
                "query1": [paper1, paper2, ...],
                "query2": [paper1, paper2, ...],
                ...
            }
        """
        logger.info(f"🔎 开始批量搜索 {len(queries)} 个查询...")
        
        results = {}
        
        for i, query in enumerate(queries, 1):
            # 如果query是字典，提取query字符串
            if isinstance(query, dict):
                query_str = query.get('query', str(query))
                perspective = query.get('perspective', 'unknown')
            else:
                query_str = str(query)
                perspective = 'unknown'
            
            logger.info(f"[{i}/{len(queries)}] 搜索: {query_str}")
            if perspective != 'unknown':
                logger.info(f"视角: {perspective}")
            
            papers = self.search(
                query=query_str,
                max_results=max_results_per_query,
                since_year=since_year
            )
            
            results[query_str] = papers
            logger.info(f"找到 {len(papers)} 篇论文")
            
            # 延迟以避免触发速率限制
            if i < len(queries):
                time.sleep(self.delay)
        
        return results
    
    def deduplicate(self, results: Dict[str, List[Dict]]) -> List[Dict]:
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
                if paper['arxiv_id'] not in seen_ids:
                    seen_ids.add(paper['arxiv_id'])
                    # 添加来源查询信息
                    paper['source_query'] = query
                    unique_papers.append(paper)
        
        return unique_papers
    
    def search_and_deduplicate(
        self,
        queries: List[str],
        max_results_per_query: int = 10,
        since_year: int = 2020
    ) -> List[Dict]:
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
        
        logger.info(f"✅ 搜索完成！总查询数: {len(queries)}, 去重前: {sum(len(papers) for papers in results.values())} 篇, 去重后: {len(unique_papers)} 篇")
        
        return unique_papers
    
    def save_to_csv(self, papers: List[Dict], output_path: str):
        """
        保存论文结果到 CSV 文件
        
        Args:
            papers: 论文列表
            output_path: 输出文件路径
        """
        if not papers:
            logger.warning("没有论文可保存")
            return
        
        # 确保输出目录存在
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            # CSV 字段
            fields = [
                'arxiv_id', 'title', 'authors', 'published', 
                'categories', 'abstract', 'pdf_url', 'arxiv_url'
            ]
            
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            
            for paper in papers:
                # 处理列表字段（作者和分类）
                row = {
                    'arxiv_id': paper['arxiv_id'],
                    'title': paper['title'],
                    'authors': '; '.join(paper['authors']),
                    'published': paper['published'],
                    'categories': '; '.join(paper['categories']),
                    'abstract': paper['abstract'],
                    'pdf_url': paper['pdf_url'],
                    'arxiv_url': paper['arxiv_url']
                }
                writer.writerow(row)
        
        logger.info(f"✅ 已保存 {len(papers)} 篇论文到: {output_path}")


# 为了向后兼容，保留原有的函数接口
def search_arxiv(query: str, max_results: int = 20, start_year: int = 2020, sort_by: str = "relevance") -> List[Dict]:
    """向后兼容的函数接口"""
    searcher = ArxivSearcher()
    return searcher.search(query, max_results, start_year, sort_by)


def search_and_deduplicate(queries: List[Dict[str, str]], max_results_per_query: int = 10, start_year: int = 2020) -> List[Dict]:
    """向后兼容的函数接口"""
    searcher = ArxivSearcher()
    return searcher.search_and_deduplicate(queries, max_results_per_query, start_year)


# 测试代码
if __name__ == "__main__":
    import json
    
    print("=" * 60)
    print("arXiv 搜索测试")
    print("=" * 60)
    
    searcher = ArxivSearcher()
    
    # 测试单个查询
    print("\n测试1: 单个查询")
    print("-" * 60)
    papers = searcher.search("transformer attention mechanism", max_results=5)
    print(f"找到 {len(papers)} 篇论文")
    if papers:
        print(f"\n第一篇论文:")
        print(json.dumps(papers[0], ensure_ascii=False, indent=2))
    
    # 测试批量查询
    print("\n\n测试2: 批量查询")
    print("-" * 60)
    test_queries = [
        "deep learning image classification",
        "convolutional neural networks"
    ]
    
    unique_papers = searcher.search_and_deduplicate(test_queries, max_results_per_query=3, since_year=2023)
    print(f"\n去重后的论文ID:")
    for paper in unique_papers:
        print(f"  - {paper['arxiv_id']}: {paper['title'][:60]}...")
