"""
LiteStorageProvider 实现

使用 SQLite 和 JSON 文件提供轻量级存储，实现 StorageProvider Protocol
"""

from __future__ import annotations

import sqlite3
import os
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .interfaces import (
    StorageProvider,
    TradeRecord,
    TradeQuery,
    LogEntry,
    LogQuery,
    DailyStats,
    LogLevel,
    LogType,
)


class SQLiteConnectionManager(BaseModel):
    """SQLite 连接管理器"""

    database_path: str

    def get_connection(self) -> sqlite3.Connection:
        """获取 SQLite 连接"""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn


class LiteStorageProvider(StorageProvider):
    """轻量级存储实现，基于 SQLite"""

    def __init__(self, trade_db_path: str, log_db_path: str):
        self.trade_db = SQLiteConnectionManager(database_path=trade_db_path)
        self.log_db = SQLiteConnectionManager(database_path=log_db_path)

        # 确保目录存在
        os.makedirs(os.path.dirname(trade_db_path), exist_ok=True)
        os.makedirs(os.path.dirname(log_db_path), exist_ok=True)

        self._init_trade_db()
        self._init_log_db()

    def _init_trade_db(self):
        """初始化交易数据库（复用 daily_limit_manager 结构）"""
        with self.trade_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS trade_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    date TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    side TEXT NOT NULL,
                    amount REAL NOT NULL,
                    price REAL NOT NULL,
                    usdt_value REAL NOT NULL,
                    fee REAL DEFAULT 0.0,
                    status TEXT NOT NULL,
                    strategy TEXT,
                    confidence TEXT,
                    notes TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_stats (
                    date TEXT PRIMARY KEY,
                    total_usdt_invested REAL DEFAULT 0.0,
                    total_usdt_withdrawn REAL DEFAULT 0.0,
                    net_usdt_flow REAL DEFAULT 0.0,
                    trade_count INTEGER DEFAULT 0,
                    successful_trades INTEGER DEFAULT 0,
                    limit_hit BOOLEAN DEFAULT FALSE,
                    reset_time DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def _init_log_db(self):
        """初始化日志数据库"""
        with self.log_db.get_connection() as conn:
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

    # ===== Trade Records =====
    def get_trade_records(self, query: TradeQuery) -> List[TradeRecord]:
        sql = "SELECT * FROM trade_records WHERE 1=1"
        params = []

        if query.symbol:
            sql += " AND symbol = ?"
            params.append(query.symbol)
        if query.side:
            sql += " AND side = ?"
            params.append(query.side)
        if query.from_date:
            sql += " AND date >= ?"
            params.append(query.from_date)
        if query.to_date:
            sql += " AND date <= ?"
            params.append(query.to_date)

        sql += " ORDER BY timestamp DESC LIMIT ?"
        params.append(query.limit)

        with self.trade_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [TradeRecord(**dict(row)) for row in rows]

    def append_trade_record(self, record: TradeRecord) -> None:
        with self.trade_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO trade_records
                (timestamp, date, symbol, side, amount, price, usdt_value,
                 fee, status, strategy, confidence, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.timestamp,
                    record.date,
                    record.symbol,
                    record.side,
                    record.amount,
                    record.price,
                    record.usdt_value,
                    record.fee,
                    record.status,
                    record.strategy,
                    record.confidence,
                    record.notes,
                ),
            )
            conn.commit()

    def get_daily_stats(self, date: Optional[str] = None) -> DailyStats:
        sql = "SELECT * FROM daily_stats WHERE date = ?"
        if date is None:
            date = datetime.utcnow().strftime("%Y-%m-%d")

        with self.trade_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (date,))
            row = cursor.fetchone()
            if row:
                stats = dict(row)
            else:
                stats = {
                    "date": date,
                    "total_usdt_invested": 0.0,
                    "total_usdt_withdrawn": 0.0,
                    "net_usdt_flow": 0.0,
                    "trade_count": 0,
                    "successful_trades": 0,
                    "limit_hit": False,
                    "daily_limit": 0.0,
                    "remaining_limit": 0.0,
                    "usage_percentage": 0.0,
                }

            return DailyStats(**stats)

    # ===== Logs =====
    def save_log(self, entry: LogEntry) -> None:
        with self.log_db.get_connection() as conn:
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
                    entry.metadata,
                ),
            )
            conn.commit()

    def query_logs(self, query: LogQuery) -> List[LogEntry]:
        sql = "SELECT * FROM app_logs WHERE 1=1"
        params = []

        if query.type:
            sql += " AND type = ?"
            params.append(query.type.value)
        if query.level:
            sql += " AND level = ?"
            params.append(query.level.value)
        if query.keyword:
            sql += " AND message LIKE ?"
            params.append(f"%{query.keyword}%")
        if query.from_time:
            sql += " AND timestamp >= ?"
            params.append(query.from_time)
        if query.to_time:
            sql += " AND timestamp <= ?"
            params.append(query.to_time)

        sql += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        limit = query.page_size
        offset = (query.page - 1) * query.page_size
        params.extend([limit, offset])

        with self.log_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [
                LogEntry(
                    id=row["id"],
                    timestamp=row["timestamp"],
                    level=LogLevel(row["level"]),
                    type=LogType(row["type"]),
                    module=row["module"],
                    message=row["message"],
                    metadata=row["metadata"],
                )
                for row in rows
            ]

    def get_log_by_id(self, log_id: int) -> Optional[LogEntry]:
        with self.log_db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM app_logs WHERE id = ?", (log_id,))
            row = cursor.fetchone()
            if row:
                return LogEntry(
                    id=row["id"],
                    timestamp=row["timestamp"],
                    level=LogLevel(row["level"]),
                    type=LogType(row["type"]),
                    module=row["module"],
                    message=row["message"],
                    metadata=row["metadata"],
                )
            return None
