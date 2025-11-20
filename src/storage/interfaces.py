"""
存储抽象接口

定义 StorageProvider、TokenRepository、LogSink 协议，支持 Lite/Enterprise 双模式
"""

from typing import Protocol, List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum


class TokenStatus(str, Enum):
    """Token 状态"""
    ACTIVE = "active"
    REVOKED = "revoked"


class LogLevel(str, Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogType(str, Enum):
    """日志类型"""
    SYSTEM = "system"
    TRADE = "trade"


class TokenInfo(BaseModel):
    """Token 信息模型"""
    token: str = Field(..., min_length=16, description="访问令牌")
    label: str = Field(..., max_length=100, description="令牌标签/说明")
    scopes: List[str] = Field(default_factory=list, description="权限范围")
    status: TokenStatus = Field(default=TokenStatus.ACTIVE, description="令牌状态")
    created_at: datetime = Field(..., description="创建时间")
    last_used_at: Optional[datetime] = Field(None, description="最后使用时间")
    expires_at: Optional[datetime] = Field(None, description="过期时间")

    class Config:
        schema_extra = {
            "example": {
                "token": "user_7b9b0c1d",
                "label": "qa observer",
                "scopes": ["logs:read", "signals:read"],
                "status": "active",
                "created_at": "2025-11-19T10:30:00Z",
                "expires_at": "2025-11-26T10:30:00Z"
            }
        }


class LogEntry(BaseModel):
    """日志条目模型"""
    id: Optional[int] = Field(None, description="日志ID")
    timestamp: datetime = Field(..., description="时间戳")
    level: LogLevel = Field(..., description="日志级别")
    type: LogType = Field(..., description="日志类型")
    module: str = Field(..., description="模块名称")
    message: str = Field(..., description="日志消息")
    metadata: Optional[Dict[str, Any]] = Field(None, description="额外元数据")

    class Config:
        schema_extra = {
            "example": {
                "timestamp": "2025-11-19T10:16:31Z",
                "level": "INFO",
                "type": "trade",
                "module": "order_executor",
                "message": "Filled BUY 0.1 BTC @ 67650.2",
                "metadata": {"order_id": "okx-12345", "strategy_id": "core-15m"}
            }
        }


class LogQuery(BaseModel):
    """日志查询条件"""
    type: Optional[LogType] = Field(None, description="日志类型过滤")
    level: Optional[LogLevel] = Field(None, description="日志级别过滤（该级别及以上）")
    keyword: Optional[str] = Field(None, description="关键字搜索")
    from_time: Optional[datetime] = Field(None, description="开始时间")
    to_time: Optional[datetime] = Field(None, description="结束时间")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=50, ge=1, le=200, description="每页数量")

    @validator("page_size")
    def validate_page_size(cls, v):
        """验证 page_size 范围"""
        if v < 1 or v > 200:
            raise ValueError("page_size must be between 1 and 200")
        return v


class TradeRecord(BaseModel):
    """交易记录模型（复用 daily_limit_manager.TradeRecord 结构）"""
    id: Optional[int] = Field(None, description="交易ID")
    timestamp: datetime = Field(..., description="交易时间")
    date: str = Field(..., description="日期（YYYY-MM-DD）")
    symbol: str = Field(..., description="交易对")
    side: str = Field(..., description="交易方向（BUY/SELL）")
    amount: float = Field(..., description="交易数量")
    price: float = Field(..., description="交易价格")
    usdt_value: float = Field(..., description="USDT价值")
    fee: float = Field(default=0.0, description="手续费")
    status: str = Field(default="completed", description="交易状态")
    strategy: str = Field(default="", description="策略标识")
    confidence: str = Field(default="MEDIUM", description="信心度")
    notes: str = Field(default="", description="备注")


class TradeQuery(BaseModel):
    """交易记录查询条件"""
    symbol: Optional[str] = Field(None, description="交易对过滤")
    side: Optional[str] = Field(None, description="交易方向过滤")
    from_date: Optional[str] = Field(None, description="开始日期（YYYY-MM-DD）")
    to_date: Optional[str] = Field(None, description="结束日期（YYYY-MM-DD）")
    limit: int = Field(default=50, ge=1, le=1000, description="返回数量限制")


class DailyStats(BaseModel):
    """日统计信息"""
    date: str = Field(..., description="日期")
    total_usdt_invested: float = Field(..., description="总投入")
    total_usdt_withdrawn: float = Field(..., description="总撤出")
    net_usdt_flow: float = Field(..., description="净流量")
    trade_count: int = Field(..., description="交易次数")
    successful_trades: int = Field(..., description="成功交易数")
    limit_hit: bool = Field(..., description="是否触发限额")
    daily_limit: float = Field(..., description="日限额")
    remaining_limit: float = Field(..., description="剩余限额")
    usage_percentage: float = Field(..., description="使用率百分比")


# ==================== Protocol Definitions ====================


class LogSink(Protocol):
    """日志写入接口"""

    def write_log(self, entry: LogEntry) -> None:
        """写入日志条目"""
        ...


class StorageProvider(Protocol):
    """存储提供者协议（支持 Lite/Enterprise 双模式）"""

    # ===== Trade Records =====
    def get_trade_records(self, query: TradeQuery) -> List[TradeRecord]:
        """
        查询交易记录

        Args:
            query: 查询条件

        Returns:
            交易记录列表
        """
        ...

    def append_trade_record(self, record: TradeRecord) -> None:
        """
        添加交易记录

        Args:
            record: 交易记录
        """
        ...

    # ===== Daily Stats =====
    def get_daily_stats(self, date: Optional[str] = None) -> DailyStats:
        """
        获取日统计数据

        Args:
            date: 日期（YYYY-MM-DD），不传则返回今日

        Returns:
            日统计信息
        """
        ...

    # ===== Logs =====
    def save_log(self, entry: LogEntry) -> None:
        """
        保存日志

        Args:
            entry: 日志条目
        """
        ...

    def query_logs(self, query: LogQuery) -> List[LogEntry]:
        """
        查询日志

        Args:
            query: 查询条件

        Returns:
            日志列表（按时间倒序）
        """
        ...

    def get_log_by_id(self, log_id: int) -> Optional[LogEntry]:
        """
        根据ID获取单条日志

        Args:
            log_id: 日志ID

        Returns:
            日志条目或 None
        """
        ...


class TokenRepository(Protocol):
    """Token 存储库协议"""

    def create_user_token(
        self,
        label: str,
        scopes: List[str],
        created_by: str,
        expires_in_hours: Optional[int] = None
    ) -> TokenInfo:
        """
        创建普通用户 Token

        Args:
            label: 令牌标签
            scopes: 权限范围
            created_by: 创建者（管理员标识）
            expires_in_hours: 过期时间（小时），None 表示永不过期

        Returns:
            Token 信息

        Raises:
            ValueError: 参数无效
        """
        ...

    def revoke_token(self, token: str) -> bool:
        """
        吊销 Token

        Args:
            token: 要吊销的 Token

        Returns:
            True: 吊销成功, False: Token 不存在
        """
        ...

    def validate_token(self, token: str) -> Optional[TokenInfo]:
        """
        验证 Token 有效性

        Args:
            token: Token 字符串

        Returns:
            TokenInfo: 有效 Token 信息, None: 无效或已过期/吊销
        """
        ...

    def list_tokens(
        self,
        status: Optional[TokenStatus] = None,
        page: int = 1,
        page_size: int = 50
    ) -> List[TokenInfo]:
        """
        列出 Token

        Args:
            status: 状态过滤（不传则返回全部）
            page: 页码
            page_size: 每页数量

        Returns:
            Token 列表（按创建时间倒序）
        """
        ...

    def update_last_used(self, token: str) -> None:
        """
        更新 Token 最后使用时间

        Args:
            token: Token 字符串

        Note:
            调用方应忽略错误（非关键操作）
        """
        ...
