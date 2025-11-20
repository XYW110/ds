"""
状态汇总路由
提供仪表盘核心数据 API
"""

from fastapi import APIRouter, Depends
from src.services.status_service import StatusService
from src.trading_engine import TradingEngine
from src.storage.lite_storage import LiteStorageProvider

router = APIRouter()


def get_status_service() -> StatusService:
    """依赖注入 StatusService"""
    return StatusService(
        engine=TradingEngine(),
        storage=LiteStorageProvider(
            trade_db_path="data/daily_limits.db",
            log_db_path="logs/app.db",
        ),
    )


@router.get("/status/summary")
def get_status_summary(service: StatusService = Depends(get_status_service)):
    """获取仪表盘汇总数据"""
    return service.get_status_summary()
