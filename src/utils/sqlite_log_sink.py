"""
SQLiteLogSink

实现将日志写入 SQLite 数据库（logs/app.db）
"""

from __future__ import annotations

import json
import os
import sqlite3
from typing import Optional

from ..storage.interfaces import LogSink, LogEntry


class SQLiteConnectionManager:
    """轻量级 SQLite 连接管理器"""

    def __init__(self, database_path: str):
        self.database_path = database_path
        os.makedirs(os.path.dirname(database_path), exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn


class SQLiteLogSink(LogSink):
    """将日志写入 SQLite 的实现"""

    def __init__(self, db_path: str):
        self.connection_manager = SQLiteConnectionManager(database_path=db_path)
        self._init_database()

    def _init_database(self):
        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS app_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    level TEXT NOT NULL,
                    type TEXT NOT NULL,
                    module TEXT NOT NULL,
                    message TEXT NOT NULL,
                    metadata TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_app_logs_timestamp ON app_logs(timestamp)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_app_logs_level ON app_logs(level)"
            )
            conn.commit()

    def write_log(self, entry: LogEntry) -> None:
        metadata_json = json.dumps(entry.metadata) if entry.metadata else None

        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO app_logs (timestamp, level, type, module, message, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    entry.timestamp,
                    entry.level.value,
                    entry.type.value,
                    entry.module,
                    entry.message,
                    metadata_json,
                ),
            )
            conn.commit()
