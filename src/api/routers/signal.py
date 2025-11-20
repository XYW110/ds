"""
信号查询路由 API 文档

该模块基于 FastAPI 提供交易信号的查询与历史回溯接口。

功能说明
- 查询最新生成的若干条交易信号（recent）
- 获取历史信号，支持按策略、信号类型、信心度、时间区间等多维度过滤
- 分页加载历史信号列表，避免返回过多记录

依赖模块
- fastapi.APIRouter              - 提供路由注册机制
- src.services.signal_service     - 实际业务逻辑实现层
- src.trading_engine.TradingEngine - 信号数据实际来源

信号结构参考
信号为 dict 类型，对应策略执行周期中的 AI 生成结果，字段示例如下：

{
  "signal": "BUY",           // 交易方向：BUY / SELL / HOLD
  "confidence": "HIGH",      // 信心程度：HIGH / MEDIUM / LOW
  "timestamp": "2025-11-19T10:15:00Z",
  "price": 67650.2,          // 触发时的价格
  "reason": "EMA crossover + bullish sentiment"
}

注意
- signal_history 在 engine 中为内存队列（长度上限由配置决定），生产环境可考虑保留 SQLite 或持久化表
- 本模块仅为只读接口，不修改信号来源

作者
- 浮浮酱 (Archon Churchill)
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from src.services.signal_service import SignalService
from src.trading_engine import TradingEngine

router = APIRouter()

def get_signal_service() -> SignalService:
    """获得信号查询服务对象"""
    return SignalService(engine=TradingEngine())

@router.get("/signals/latest")
def latest_signals(
    limit: int = Query(30, ge=1, le=100, description="最多返回的手术数"),
    service: SignalService = Depends(get_signal_service)
):
    """获取最近生成的策略信号列表"""
    return {"signals": service.get_latest_signals(limit=limit)}

@router.get("/signals/history")
def signal_history(
    strategy_id: Optional[str] = Query(None, description="按策略ID过滤"),
    signal_type: Optional[str] = Query(None, description="按信号类型过滤（BUY/SELL/HOLD）"),
    confidence: Optional[str] = Query(None, description="信心度过滤"),
    from_time: Optional[datetime] = None,
    to_time: Optional[datetime] = None,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=200, description="单页记录数"),
    service: SignalService = Depends(get_signal_service)
):
    """分页获取历史信号记录，支持按条件过滤"""
    return service.get_signal_history(
        strategy_id=strategy_id,
        signal_type=signal_type,
        confidence=confidence,
        from_time=from_time,
        to_time=to_time,
        page=page,
        page_size=page_size
    )
