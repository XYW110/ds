"""
日志服务
封装日志查询和存储逻辑
"""

from datetime import datetime
from typing import List, Optional

from ..storage.interfaces import (
    StorageProvider,
    LogEntry,
    LogQuery,
    LogLevel,
    LogType,
)


class LogService:
    """日志服务，提供查询和存储接口"""

    def __init__(self, storage: StorageProvider):
        self.storage = storage

    def query_logs(
        self,
        log_type: Optional[str] = None,
        level: Optional[str] = None,
        keyword: Optional[str] = None,
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> dict:
        """查询日志，支持多条件过滤和分页"""
        query = LogQuery(
            type=LogType(log_type) if log_type else None,
            level=LogLevel(level) if level else None,
            keyword=keyword,
            from_time=from_time,
            to_time=to_time,
            page=page,
            page_size=page_size,
        )

        logs = self.storage.query_logs(query)

        return {
            "logs": [log.dict() for log in logs],
            "total": len(logs),
            "page": page,
            "page_size": page_size,
        }

    def save_log(
        self,
        level: str,
        message: str,
        module: str,
        log_type: str = "system",
        metadata: Optional[dict] = None,
    ) -> None:
        """保存单条日志"""
        entry = LogEntry(
            timestamp=datetime.utcnow(),
            level=LogLevel(level),
            type=LogType(log_type),
            module=module,
            message=message,
            metadata=metadata,
        )
        self.storage.save_log(entry)

