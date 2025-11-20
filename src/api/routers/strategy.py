"""
策略管理路由
"""

from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ...services.strategy_service import StrategyService
from ...trading_engine import TradingEngine

router = APIRouter()


class UpdateParamsRequest(BaseModel):
    """更新参数请求"""
    params: Dict[str, Any]


def get_strategy_service() -> StrategyService:
    """依赖注入 StrategyService"""
    return StrategyService(engine=TradingEngine())


@router.get("/strategy")
def list_strategies(service: StrategyService = Depends(get_strategy_service)):
    """列出所有策略"""
    return {"strategies": service.get_all_strategies()}


@router.get("/strategy/{strategy_id}")
def get_strategy(
    strategy_id: str,
    service: StrategyService = Depends(get_strategy_service)
):
    """获取策略详情"""
    try:
        return service.get_strategy(strategy_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/strategy/{strategy_id}/start")
def start_strategy(
    strategy_id: str,
    service: StrategyService = Depends(get_strategy_service)
):
    """启动策略"""
    try:
        result = service.start_strategy(strategy_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/strategy/{strategy_id}/stop")
def stop_strategy(
    strategy_id: str,
    service: StrategyService = Depends(get_strategy_service)
):
    """停止策略"""
    try:
        result = service.stop_strategy(strategy_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/strategy/{strategy_id}/params")
def update_strategy_params(
    strategy_id: str,
    request: UpdateParamsRequest,
    service: StrategyService = Depends(get_strategy_service)
):
    """更新策略参数"""
    try:
        result = service.update_strategy_params(strategy_id, request.params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
