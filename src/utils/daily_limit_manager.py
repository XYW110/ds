"""
日投入限额管理器

提供每日交易投入限额的控制功能，包括：
- 交易记录跟踪
- 日累计投入计算
- 限额检测和阻止
- 数据持久化存储
- 时间处理和重置逻辑
"""

import sqlite3
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
import pytz
from ..utils.logger import get_logger


@dataclass
class TradeRecord:
    """交易记录数据结构"""
    id: Optional[int] = None
    timestamp: Optional[datetime] = None
    date: str = ""  # YYYY-MM-DD格式
    symbol: str = ""
    side: str = ""  # BUY/SELL
    amount: float = 0.0  # 交易数量
    price: float = 0.0  # 交易价格
    usdt_value: float = 0.0  # USDT价值
    fee: float = 0.0  # 手续费
    status: str = "completed"  # completed/cancelled/failed
    strategy: str = ""  # 策略标识
    confidence: str = "MEDIUM"  # 信心度
    notes: str = ""  # 备注


class DailyLimitManager:
    """日投入限额管理器"""

    def __init__(self, config):
        """
        初始化日投入限额管理器

        Args:
            config: DailyLimitConfig配置对象
        """
        self.config = config
        self.logger = get_logger(__name__)

        # 创建数据库目录
        db_dir = os.path.dirname(config.database_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        # 初始化数据库
        self._init_database()

        # 时区处理
        try:
            self.timezone = pytz.timezone(config.reset_timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            self.logger.warning(f"未知时区 {config.reset_timezone}，使用UTC")
            self.timezone = pytz.UTC

    def _init_database(self):
        """初始化SQLite数据库"""
        try:
            with sqlite3.connect(self.config.database_path) as conn:
                cursor = conn.cursor()

                # 创建交易记录表
                cursor.execute('''
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
                ''')

                # 创建索引
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_trade_records_date ON trade_records(date)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_trade_records_status ON trade_records(status)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_trade_records_timestamp ON trade_records(timestamp)')

                # 创建日统计表
                cursor.execute('''
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
                ''')

                conn.commit()
                self.logger.info("日投入限额数据库初始化成功")

        except sqlite3.Error as e:
            self.logger.error(f"数据库初始化失败: {e}")
            raise

    def get_current_date(self) -> str:
        """
        获取当前日期（考虑时区）

        Returns:
            str: YYYY-MM-DD格式的日期字符串
        """
        now_utc = datetime.now(timezone.utc)
        now_local = now_utc.astimezone(self.timezone)
        return now_local.strftime('%Y-%m-%d')

    def get_next_reset_time(self) -> datetime:
        """
        获取下次重置时间

        Returns:
            datetime: 下次重置时间（UTC）
        """
        now_utc = datetime.now(timezone.utc)
        now_local = now_utc.astimezone(self.timezone)

        # 计算今天的重置时间
        reset_time_local = now_local.replace(
            hour=self.config.reset_hour,
            minute=0,
            second=0,
            microsecond=0
        )

        # 如果当前时间已经过了今天的重置时间，则设置为明天
        if now_local >= reset_time_local:
            reset_time_local += timedelta(days=1)

        # 转换为UTC返回
        reset_time_utc = reset_time_local.astimezone(timezone.utc)
        return reset_time_utc

    def should_reset_daily_limit(self) -> bool:
        """
        检查是否应该重置日限额

        Returns:
            bool: 是否需要重置
        """
        try:
            current_date = self.get_current_date()

            with sqlite3.connect(self.config.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT date FROM daily_stats WHERE date = ? LIMIT 1",
                    (current_date,)
                )
                result = cursor.fetchone()

                # 如果今天还没有记录，说明需要重置
                return result is None

        except sqlite3.Error as e:
            self.logger.error(f"检查重置状态失败: {e}")
            return False

    def reset_daily_limit(self):
        """重置日限额统计"""
        try:
            current_date = self.get_current_date()
            next_reset = self.get_next_reset_time()

            with sqlite3.connect(self.config.database_path) as conn:
                cursor = conn.cursor()

                # 插入或更新今日统计
                cursor.execute('''
                    INSERT OR REPLACE INTO daily_stats
                    (date, total_usdt_invested, total_usdt_withdrawn, net_usdt_flow,
                     trade_count, successful_trades, limit_hit, reset_time, updated_at)
                    VALUES (?, 0.0, 0.0, 0.0, 0, 0, FALSE, ?, CURRENT_TIMESTAMP)
                ''', (current_date, next_reset))

                conn.commit()
                self.logger.info(f"日限额已重置，日期: {current_date}")

        except sqlite3.Error as e:
            self.logger.error(f"重置日限额失败: {e}")
            raise

    def get_daily_stats(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        获取日统计数据

        Args:
            date: 日期字符串，默认为今天

        Returns:
            Dict[str, Any]: 日统计信��
        """
        if date is None:
            date = self.get_current_date()

        try:
            with sqlite3.connect(self.config.database_path) as conn:
                cursor = conn.cursor()

                # 获取统计数据
                cursor.execute(
                    "SELECT * FROM daily_stats WHERE date = ?",
                    (date,)
                )
                stats_row = cursor.fetchone()

                if stats_row:
                    columns = [desc[0] for desc in cursor.description]
                    stats = dict(zip(columns, stats_row))
                else:
                    # 如果没有统计数据，返回默认值
                    stats = {
                        'date': date,
                        'total_usdt_invested': 0.0,
                        'total_usdt_withdrawn': 0.0,
                        'net_usdt_flow': 0.0,
                        'trade_count': 0,
                        'successful_trades': 0,
                        'limit_hit': False,
                        'reset_time': self.get_next_reset_time()
                    }

                # 计算剩余限额
                remaining_limit = max(0, self.config.daily_limit_usdt - stats['total_usdt_invested'])
                usage_percentage = min(1.0, stats['total_usdt_invested'] / self.config.daily_limit_usdt) if self.config.daily_limit_usdt > 0 else 0

                stats.update({
                    'daily_limit': self.config.daily_limit_usdt,
                    'remaining_limit': remaining_limit,
                    'usage_percentage': usage_percentage,
                    'is_warning_threshold': usage_percentage >= self.config.warning_threshold
                })

                return stats

        except sqlite3.Error as e:
            self.logger.error(f"获取日统计失败: {e}")
            return {}

    def record_trade(self, trade_record: TradeRecord) -> bool:
        """
        记录交易数据

        Args:
            trade_record: 交易记录对象

        Returns:
            bool: 记录是否成功
        """
        try:
            # 确保记录有正确的日期
            if trade_record.date == "":
                trade_record.date = self.get_current_date()

            if trade_record.timestamp is None:
                trade_record.timestamp = datetime.now(timezone.utc)

            with sqlite3.connect(self.config.database_path) as conn:
                cursor = conn.cursor()

                # 插入交易记录
                cursor.execute('''
                    INSERT INTO trade_records
                    (timestamp, date, symbol, side, amount, price, usdt_value,
                     fee, status, strategy, confidence, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    trade_record.timestamp,
                    trade_record.date,
                    trade_record.symbol,
                    trade_record.side,
                    trade_record.amount,
                    trade_record.price,
                    trade_record.usdt_value,
                    trade_record.fee,
                    trade_record.status,
                    trade_record.strategy,
                    trade_record.confidence,
                    trade_record.notes
                ))

                # 更新日统计（仅对成功的交易）
                if trade_record.status == "completed":
                    self._update_daily_stats(cursor, trade_record)

                conn.commit()
                self.logger.info(f"交易记录已保存: {trade_record.symbol} {trade_record.side} {trade_record.usdt_value:.2f} USDT")
                return True

        except sqlite3.Error as e:
            self.logger.error(f"记录交易失败: {e}")
            return False

    def _update_daily_stats(self, cursor, trade_record: TradeRecord):
        """更新日统计数据"""
        current_date = trade_record.date

        # 获取当前统计
        cursor.execute(
            "SELECT * FROM daily_stats WHERE date = ?",
            (current_date,)
        )
        stats_row = cursor.fetchone()

        if stats_row:
            # 更新现有记录
            columns = [desc[0] for desc in cursor.description]
            stats = dict(zip(columns, stats_row))

            new_invested = stats['total_usdt_invested']
            new_withdrawn = stats['total_usdt_withdrawn']

            # 根据交易方向更新投入/撤出
            if trade_record.side.upper() == "BUY":
                new_invested += trade_record.usdt_value
            elif trade_record.side.upper() == "SELL":
                new_withdrawn += trade_record.usdt_value

            net_flow = new_invested - new_withdrawn
            trade_count = stats['trade_count'] + 1
            successful_trades = stats['successful_trades'] + 1
            limit_hit = new_invested >= self.config.daily_limit_usdt

            cursor.execute('''
                UPDATE daily_stats
                SET total_usdt_invested = ?, total_usdt_withdrawn = ?, net_usdt_flow = ?,
                    trade_count = ?, successful_trades = ?, limit_hit = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE date = ?
            ''', (new_invested, new_withdrawn, net_flow, trade_count,
                  successful_trades, limit_hit, current_date))
        else:
            # 创建新记录
            new_invested = trade_record.usdt_value if trade_record.side.upper() == "BUY" else 0.0
            new_withdrawn = trade_record.usdt_value if trade_record.side.upper() == "SELL" else 0.0
            net_flow = new_invested - new_withdrawn
            limit_hit = new_invested >= self.config.daily_limit_usdt

            cursor.execute('''
                INSERT INTO daily_stats
                (date, total_usdt_invested, total_usdt_withdrawn, net_usdt_flow,
                 trade_count, successful_trades, limit_hit, reset_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (current_date, new_invested, new_withdrawn, net_flow,
                  1, 1, limit_hit, self.get_next_reset_time()))

    def check_trade_limit(self, proposed_usdt_amount: float, trade_side: str = "BUY") -> Tuple[bool, str]:
        """
        检查交易是否会超过日限额

        Args:
            proposed_usdt_amount: 建议投入的USDT金额
            trade_side: 交易方向 (BUY/SELL)

        Returns:
            Tuple[bool, str]: (是否允许交易, 原因说明)
        """
        if not self.config.enable:
            return True, "日投入限额功能已禁用"

        # SELL交易通常不受投入限额限制
        if trade_side.upper() == "SELL":
            return True, "卖出交易不受投入限额限制"

        # 检查是否需要重置
        if self.should_reset_daily_limit():
            self.reset_daily_limit()

        # 获取当前统计
        stats = self.get_daily_stats()
        current_invested = stats.get('total_usdt_invested', 0.0)

        # 检查是否会超过限额
        if current_invested + proposed_usdt_amount > self.config.daily_limit_usdt:
            remaining = self.config.daily_limit_usdt - current_invested
            return False, f"超过日投入限额！当前已投入: {current_invested:.2f} USDT，剩余: {remaining:.2f} USDT，建议: {proposed_usdt_amount:.2f} USDT"

        # 检查是否接近警告阈值
        usage_percentage = (current_invested + proposed_usdt_amount) / self.config.daily_limit_usdt
        if usage_percentage >= self.config.warning_threshold:
            self.logger.warning(f"接近日投入限额警告: {usage_percentage*100:.1f}%")
            return True, f"警告：交易后将达到日限额的 {usage_percentage*100:.1f}%"

        return True, "交易在日投入限额范围内"

    def get_trade_history(self, limit: int = 50, date: Optional[str] = None) -> List[TradeRecord]:
        """
        获取交易历史记录

        Args:
            limit: 返回记录数量限制
            date: 指定日期，默认为所有日期

        Returns:
            List[TradeRecord]: 交易记录列表
        """
        try:
            with sqlite3.connect(self.config.database_path) as conn:
                cursor = conn.cursor()

                if date:
                    cursor.execute('''
                        SELECT * FROM trade_records
                        WHERE date = ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    ''', (date, limit))
                else:
                    cursor.execute('''
                        SELECT * FROM trade_records
                        ORDER BY timestamp DESC
                        LIMIT ?
                    ''', (limit,))

                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                records = []
                for row in rows:
                    row_dict = dict(zip(columns, row))
                    record = TradeRecord(
                        id=row_dict['id'],
                        timestamp=datetime.fromisoformat(row_dict['timestamp']) if row_dict['timestamp'] else None,
                        date=row_dict['date'],
                        symbol=row_dict['symbol'],
                        side=row_dict['side'],
                        amount=row_dict['amount'],
                        price=row_dict['price'],
                        usdt_value=row_dict['usdt_value'],
                        fee=row_dict['fee'],
                        status=row_dict['status'],
                        strategy=row_dict['strategy'] or "",
                        confidence=row_dict['confidence'] or "MEDIUM",
                        notes=row_dict['notes'] or ""
                    )
                    records.append(record)

                return records

        except sqlite3.Error as e:
            self.logger.error(f"获取交易历史失败: {e}")
            return []

    def cleanup_old_data(self, days_to_keep: int = 30):
        """
        清理旧数据

        Args:
            days_to_keep: 保留天数
        """
        try:
            cutoff_date = (datetime.now(timezone.utc) - timedelta(days=days_to_keep)).strftime('%Y-%m-%d')

            with sqlite3.connect(self.config.database_path) as conn:
                cursor = conn.cursor()

                # 删除旧交易记录
                cursor.execute(
                    "DELETE FROM trade_records WHERE date < ?",
                    (cutoff_date,)
                )

                # 删除旧统计数据
                cursor.execute(
                    "DELETE FROM daily_stats WHERE date < ?",
                    (cutoff_date,)
                )

                deleted_count = cursor.rowcount
                conn.commit()

                self.logger.info(f"已清理 {deleted_count} 条旧数据（保留最近 {days_to_keep} 天）")

        except sqlite3.Error as e:
            self.logger.error(f"清理旧数据失败: {e}")

    def get_summary_report(self) -> Dict[str, Any]:
        """
        获取汇总报告

        Returns:
            Dict[str, Any]: 汇总报告数据
        """
        try:
            current_date = self.get_current_date()
            today_stats = self.get_daily_stats(current_date)

            # 获取最近7天的统计
            with sqlite3.connect(self.config.database_path) as conn:
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT date, total_usdt_invested, total_usdt_withdrawn, net_usdt_flow,
                           trade_count, successful_trades, limit_hit
                    FROM daily_stats
                    WHERE date >= date('now', '-7 days')
                    ORDER BY date DESC
                ''')

                recent_days = []
                columns = ['date', 'total_usdt_invested', 'total_usdt_withdrawn',
                          'net_usdt_flow', 'trade_count', 'successful_trades', 'limit_hit']

                for row in cursor.fetchall():
                    day_stats = dict(zip(columns, row))
                    recent_days.append(day_stats)

                # 计算总计
                total_invested_7d = sum(day['total_usdt_invested'] for day in recent_days)
                total_trades_7d = sum(day['trade_count'] for day in recent_days)
                successful_trades_7d = sum(day['successful_trades'] for day in recent_days)

                return {
                    'current_date': current_date,
                    'today_stats': today_stats,
                    'next_reset_time': self.get_next_reset_time(),
                    'recent_7_days': recent_days,
                    'summary_7_days': {
                        'total_invested': total_invested_7d,
                        'total_trades': total_trades_7d,
                        'successful_trades': successful_trades_7d,
                        'success_rate': (successful_trades_7d / total_trades_7d * 100) if total_trades_7d > 0 else 0
                    },
                    'config': {
                        'daily_limit_usdt': self.config.daily_limit_usdt,
                        'reset_hour': self.config.reset_hour,
                        'timezone': self.config.reset_timezone,
                        'warning_threshold': self.config.warning_threshold
                    }
                }

        except sqlite3.Error as e:
            self.logger.error(f"生成汇总报告失败: {e}")
            return {}