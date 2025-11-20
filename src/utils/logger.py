"""
日志系统模块

提供统一的日志记录功能。
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from typing import Optional, List

from ..storage.interfaces import LogEntry, LogLevel, LogType
from .sqlite_log_sink import SQLiteLogSink

LOGS_DIR = os.path.join(os.getcwd(), "logs")
LOG_FILE = os.path.join(LOGS_DIR, "app.log")
LOG_DB = os.path.join(LOGS_DIR, "app.db")


class MultiSinkHandler(logging.Handler):
    """同时写入多个 Sink 的 Handler"""

    def __init__(self, sinks: List[SQLiteLogSink]):
        super().__init__()
        self.sinks = sinks

    def emit(self, record: logging.LogRecord) -> None:
        try:
            entry = LogEntry(
                timestamp=datetime.utcfromtimestamp(record.created),
                level=LogLevel(record.levelname),
                type=LogType.SYSTEM,
                module=record.name,
                message=record.getMessage(),
                metadata={
                    "pathname": record.pathname,
                    "lineno": record.lineno,
                },
            )
            for sink in self.sinks:
                sink.write_log(entry)
        except Exception:
            self.handleError(record)


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

    os.makedirs(LOGS_DIR, exist_ok=True)

    if level is None:
        level = logging.INFO
    logger.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight', backupCount=7, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    sqlite_sink = SQLiteLogSink(LOG_DB)
    multi_handler = MultiSinkHandler([sqlite_sink])
    multi_handler.setLevel(level)
    multi_handler.setFormatter(formatter)
    logger.addHandler(multi_handler)

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