"""
状态汇总服务
聚合交易机器人的整体运行状态，供仪表盘展示
"""

from datetime import datetime
from typing import Dict, Any

from ..trading_engine import TradingEngine
from ..utils.logger import get_logger
from ..storage.lite_storage import LiteStorageProvider


class StatusService:
    """状态服务，聚合多维度数据"""

    def __init__(self, engine: TradingEngine, storage: LiteStorageProvider):
        self.engine = engine
        self.storage = storage
        self.logger = get_logger(__name__)

    def get_status_summary(self, user_role: str = "user") -> Dict[str, Any]:
        """获取状态汇总

        Args:
            user_role: 用户角色（admin/user），控制数据可见性

        Returns:
            完整的状态汇总字典
        """
        try:
            # 获取交易引擎状态
            engine_status = self.engine.get_status()

            # 获取日限额统计
            daily_stats = self.storage.get_daily_stats()

            # 构建响应
            summary = {
                "timestamp": datetime.utcnow().isoformat(),
                "engine": {
                    "id": engine_status["id"],
                    "status": engine_status["status"],
                    "running": engine_status["running"],
                    "config": engine_status["config"],
                },
                "signals": {
                    "total_count": engine_status["signal_history_count"],
                    "recent": engine_status["recent_signals"],
                },
                "daily_limit": {
                    "limit_usdt": daily_stats.daily_limit,
                    "used": daily_stats.total_usdt_invested,
                    "remaining": daily_stats.remaining_limit,
                    "usage_pct": round(daily_stats.usage_percentage * 100, 2),
                },
                "stats": {
                    "order_stats": engine_status.get("order_stats", {}),
                    "frequency_stats": engine_status.get("frequency_stats", {}),
                },
            }

            return summary

        except Exception as e:
            self.logger.error(f"获取状态汇总失败: {e}")
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "error": f"Failed to retrieve status: {e}",
                "engine": {"status": "error"},
            }
