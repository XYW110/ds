"""
策略服务
封装 TradingEngine 的策略控制逻辑
"""

from typing import Dict, Any, List

from ..trading_engine import TradingEngine
from ..utils.logger import get_logger


class StrategyService:
    def __init__(self, engine: TradingEngine):
        self.engine = engine
        self.logger = get_logger(__name__)

    def get_all_strategies(self) -> List[Dict[str, Any]]:
        """获取所有策略（当前只有一个）"""
        return [self.engine.get_status()]

    def get_strategy(self, strategy_id: str) -> Dict[str, Any]:
        """获取指定策略详情"""
        if strategy_id != self.engine.strategy_id:
            raise ValueError(f"策略 {strategy_id} 不存在")
        return self.engine.get_status()

    def start_strategy(self, strategy_id: str) -> Dict[str, Any]:
        """启动策略"""
        if strategy_id != self.engine.strategy_id:
            raise ValueError(f"策略 {strategy_id} 不存在")

        success = self.engine.start()
        self.logger.info(f"策略 {strategy_id} 启动操作: {'成功' if success else '失败'}")

        return {
            "success": success,
            "strategy_id": strategy_id,
            "status": "running" if success else self.engine.get_status()["status"],
            "message": "策略已启动" if success else "策略已在运行中"
        }

    def stop_strategy(self, strategy_id: str) -> Dict[str, Any]:
        """停止策略"""
        if strategy_id != self.engine.strategy_id:
            raise ValueError(f"策略 {strategy_id} 不存在")

        success = self.engine.stop()
        self.logger.info(f"策略 {strategy_id} 停止操作: {'成功' if success else '失败'}")

        return {
            "success": success,
            "strategy_id": strategy_id,
            "status": "stopped" if success else self.engine.get_status()["status"],
            "message": "策略已停止" if success else "策略未在运行"
        }

    def update_strategy_params(self, strategy_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """更新策略参数"""
        if strategy_id != self.engine.strategy_id:
            raise ValueError(f"策略 {strategy_id} 不存在")

        updated = self.engine.update_config(params)
        self.logger.info(f"策略 {strategy_id} 参数更新: {updated}")

        return {
            "success": True,
            "strategy_id": strategy_id,
            "updated_params": updated,
            "message": "参数更新成功"
        }
