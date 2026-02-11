"""
学术搜索引擎抽象基类
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

from literature_review.logger import get_logger


class BaseSearcher(ABC):
    """学术搜索引擎抽象基类"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化搜索器

        Args:
            config: 搜索引擎配置字典
        """
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        self.max_retries = config.get('max_retries', 3)
        self.delay = config.get('delay', 5)
        self.timeout = config.get('timeout', 30)

        self.logger.info(f"初始化 {self.__class__.__name__}: max_retries={self.max_retries}, delay={self.delay}s")

    @abstractmethod
    def search(
        self,
        query: str,
        max_results: int = 10,
        since_year: int = 2020
    ) -> List[Dict[str, Any]]:
        """
        搜索论文

        Args:
            query: 搜索查询字符串
            max_results: 最大结果数
            since_year: 起始年份

        Returns:
            标准化的论文列表，每篇论文包含:
            - id: 论文唯一标识
            - title: 标题
            - authors: 作者列表 (List[str])
            - published: 发表日期 (YYYY-MM-DD)
            - abstract: 摘要
            - url: 论文链接
            - source: 来源 (arxiv/semantic_scholar/crossref)
        """
        pass

    @abstractmethod
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
            {
                "query1": [paper1, paper2, ...],
                "query2": [paper1, paper2, ...],
            }
        """
        pass

    def normalize_paper(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化论文格式（子类可选实现）

        Args:
            paper: 原始论文数据

        Returns:
            标准化后的论文数据
        """
        return paper
