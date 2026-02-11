"""
搜索引擎配置管理模块
"""
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

from literature_review.logger import get_logger

logger = get_logger("search_config")


class SearchConfig:
    """搜索引擎配置管理器"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径，默认使用 config/search_config.yaml
        """
        if config_path is None:
            config_path = Path(__file__).parent / "search_config.yaml"
        else:
            config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        logger.info(f"加载搜索引擎配置: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        logger.info(f"当前选择的搜索引擎: {self.get_selected_engine()}")

    def get_selected_engine(self) -> str:
        """获取当前选择的搜索引擎"""
        return self.config['SEARCH_ENGINE']['selected']

    def get_engine_config(self, engine_name: str) -> Dict[str, Any]:
        """
        获取指定搜索引擎的配置

        Args:
            engine_name: 搜索引擎名称（arxiv, semantic_scholar, crossref）

        Returns:
            搜索引擎配置字典
        """
        return self.config['SEARCH_ENGINE'].get(engine_name, {})

    def is_multi_engine_enabled(self) -> bool:
        """检查是否启用多引擎模式"""
        return self.config['SEARCH_ENGINE']['multi_engine']['enabled']

    def get_multi_engine_config(self) -> Dict[str, Any]:
        """获取多引擎模式配置"""
        return self.config['SEARCH_ENGINE']['multi_engine']
