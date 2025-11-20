"""
信号查询服务
提供交易信号的查询和过滤功能
"""

from datetime import datetime
from typing import Dict, Any, List, Optional

from ..trading_engine import TradingEngine
from ..utils.logger import get_logger


class SignalService:
    def __init__(self, engine: TradingEngine):
        self.engine = engine
        self.logger = get_logger(__name__)

    def get_latest_signals(self, limit: int = 30) -> List[Dict[str, Any]]:
        """获取最新的 N 条信号"""
        signals = self.engine.signal_history[-limit:] if self.engine.signal_history else []
        return list(reversed(signals))  # 按时间倒序

    def get_signal_history(
        self,
        strategy_id: Optional[str] = None,
        signal_type: Optional[str] = None,
        confidence: Optional[str] = None,
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 50
    ) -> Dict[str, Any]:
        """获取信号历史，支持多种过滤条件"""
        all_signals = self.engine.signal_history

        # 过滤条件
        filtered_signals = []
        for signal in all_signals:
            # 策略ID过滤
            if strategy_id and signal.get("strategy_id") != strategy_id:
                continue

            # 信号类型过滤
            if signal_type and signal.get("signal") != signal_type:
                continue

            # 信心度过滤
            if confidence and signal.get("confidence") != confidence:
                continue

            # 时间范围过滤
            signal_time = signal.get("timestamp")
            if from_time and signal_time < from_time:
                continue
            if to_time and signal_time > to_time:
                continue

            filtered_signals.append(signal)

        # 按时间倒序排序
        filtered_signals.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        # 分页
        total = len(filtered_signals)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_signals = filtered_signals[start:end]

        return {
            "signals": paginated_signals,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
