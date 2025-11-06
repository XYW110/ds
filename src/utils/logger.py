"""
日志系统模块

提供统一的日志记录功能。
"""

import logging
import sys
from typing import Optional


def get_logger(name: str = 'deepseek_bot', level: Optional[int] = None) -> logging.Logger:
    """
    获取日志记录器

    Args:
        name: 日志记录器名称
        level: 日志级别

    Returns:
        logging.Logger: 日志记录器
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    # 设置日志级别
    if level is None:
        level = logging.INFO
    logger.setLevel(level)

    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def setup_logging(level: str = 'INFO') -> logging.Logger:
    """
    设置全局日志配置

    Args:
        level: 日志级别字符串

    Returns:
        logging.Logger: 主日志记录器
    """
    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    level_int = log_levels.get(level.upper(), logging.INFO)
    return get_logger('deepseek_bot', level_int)