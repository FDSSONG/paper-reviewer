#!/usr/bin/env python3
"""
日志系统 - 集中配置模块
提供统一的日志初始化和获取接口
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logger(
    name: str = "literature_review",
    log_dir: str = None,
    level: int = logging.INFO,
    max_bytes: int = 5 * 1024 * 1024,  # 5MB
    backup_count: int = 3
) -> logging.Logger:
    """
    初始化根 logger
    
    Args:
        name: logger 名称
        log_dir: 日志文件输出目录（None 则只输出到控制台）
        level: 日志级别
        max_bytes: 单个日志文件最大字节数
        backup_count: 保留的旧日志文件数量
    
    Returns:
        配置好的 Logger 实例
    """
    logger = logging.getLogger(name)
    
    # 防止重复添加 handler
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)  # logger 本身接收所有级别

    # 格式：时间 | 级别 | 模块名 | 消息
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S"
    )

    # 控制台输出
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(level)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # 文件输出（自动轮转）
    if log_dir:
        log_path = Path(log_dir) / "pipeline.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            str(log_path),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
        logger.info(f"日志文件: {log_path}")

    return logger


def get_logger(module_name: str) -> logging.Logger:
    """
    获取子模块 logger
    
    各模块顶部调用：
        from literature_review.logger import get_logger
        logger = get_logger("模块名")
    
    Args:
        module_name: 模块名（如 "arxiv_searcher"）
    
    Returns:
        子 Logger 实例（继承根 logger 的 handler 配置）
    """
    return logging.getLogger(f"literature_review.{module_name}")
