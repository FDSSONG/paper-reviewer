"""
搜索引擎工厂模块
根据配置文件动态创建搜索引擎实例
"""
from typing import Optional

from literature_review.config import SearchConfig
from literature_review.searchers.base_searcher import BaseSearcher
from literature_review.searchers.arxiv_searcher import ArxivSearcher
from literature_review.searchers.semantic_scholar_searcher import SemanticScholarSearcher
from literature_review.searchers.crossref_searcher import CrossRefSearcher
from literature_review.logger import get_logger

logger = get_logger("search_factory")


class SearchEngineFactory:
    """搜索引擎工厂类"""

    # 注册的搜索引擎映射
    _ENGINES = {
        'arxiv': ArxivSearcher,
        'semantic_scholar': SemanticScholarSearcher,
        'crossref': CrossRefSearcher,
    }

    @classmethod
    def create_searcher(
        cls,
        engine_name: Optional[str] = None,
        config: Optional[SearchConfig] = None
    ) -> BaseSearcher:
        """
        创建搜索引擎实例

        Args:
            engine_name: 搜索引擎名称，如果为 None 则从配置文件读取
            config: SearchConfig 实例，如果为 None 则创建新实例

        Returns:
            BaseSearcher 实例

        Raises:
            ValueError: 如果搜索引擎不支持
        """
        # 加载配置
        if config is None:
            config = SearchConfig()

        # 确定使用哪个搜索引擎
        if engine_name is None:
            engine_name = config.get_selected_engine()

        logger.info(f"创建搜索引擎: {engine_name}")

        # 检查是否支持该搜索引擎
        if engine_name not in cls._ENGINES:
            supported = ', '.join(cls._ENGINES.keys())
            raise ValueError(
                f"不支持的搜索引擎: {engine_name}。"
                f"支持的搜索引擎: {supported}"
            )

        # 获取搜索引擎配置
        engine_config = config.get_engine_config(engine_name)

        # 创建搜索引擎实例
        searcher_class = cls._ENGINES[engine_name]
        searcher = searcher_class(engine_config)

        logger.info(f"✅ {engine_name} 搜索引擎创建成功")
        return searcher

    @classmethod
    def create_multi_searchers(
        cls,
        config: Optional[SearchConfig] = None
    ) -> list[BaseSearcher]:
        """
        创建多个搜索引擎实例（用于多引擎模式）

        Args:
            config: SearchConfig 实例，如果为 None 则创建新实例

        Returns:
            BaseSearcher 实例列表
        """
        # 加载配置
        if config is None:
            config = SearchConfig()

        # 检查是否启用多引擎模式
        if not config.is_multi_engine_enabled():
            logger.warning("多引擎模式未启用，返回单个搜索引擎")
            return [cls.create_searcher(config=config)]

        # 获取多引擎配置
        multi_config = config.get_multi_engine_config()
        engine_names = multi_config.get('engines', [])

        logger.info(f"创建多个搜索引擎: {engine_names}")

        searchers = []
        for engine_name in engine_names:
            try:
                searcher = cls.create_searcher(engine_name=engine_name, config=config)
                searchers.append(searcher)
            except ValueError as e:
                logger.error(f"创建搜索引擎失败: {e}")
                continue

        logger.info(f"✅ 成功创建 {len(searchers)} 个搜索引擎")
        return searchers

    @classmethod
    def register_engine(cls, name: str, searcher_class: type):
        """
        注册新的搜索引擎

        Args:
            name: 搜索引擎名称
            searcher_class: 搜索引擎类（必须继承自 BaseSearcher）
        """
        if not issubclass(searcher_class, BaseSearcher):
            raise TypeError(f"{searcher_class} 必须继承自 BaseSearcher")

        cls._ENGINES[name] = searcher_class
        logger.info(f"注册搜索引擎: {name}")


# 便捷函数
def create_searcher(
    engine_name: Optional[str] = None,
    config: Optional[SearchConfig] = None
) -> BaseSearcher:
    """
    创建搜索引擎实例（便捷函数）

    Args:
        engine_name: 搜索引擎名称，如果为 None 则从配置文件读取
        config: SearchConfig 实例，如果为 None 则创建新实例

    Returns:
        BaseSearcher 实例
    """
    return SearchEngineFactory.create_searcher(engine_name, config)


def create_multi_searchers(
    config: Optional[SearchConfig] = None
) -> list[BaseSearcher]:
    """
    创建多个搜索引擎实例（便捷函数）

    Args:
        config: SearchConfig 实例，如果为 None 则创建新实例

    Returns:
        BaseSearcher 实例列表
    """
    return SearchEngineFactory.create_multi_searchers(config)
