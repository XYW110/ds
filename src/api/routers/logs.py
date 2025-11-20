"""日志查询路由"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ...services.log_service import LogService
from ...storage.lite_storage import LiteStorageProvider

router = APIRouter()


class LogResponse(BaseModel):
    logs: list
    total: int
    page: int
    page_size: int


def get_log_service():
    """依赖注入 LogService"""
    storage = LiteStorageProvider(
        trade_db_path="data/daily_limits.db",
        log_db_path="logs/app.db",
    )
    return LogService(storage=storage)


@router.get("/logs", response_model=LogResponse)
def get_logs(
    type: Optional[str] = Query(None, description="日志类型：system/trade"),
    level: Optional[str] = Query(None, description="日志级别：DEBUG/INFO/WARNING/ERROR/CRITICAL"),
    keyword: Optional[str] = Query(None, description="关键字搜索，匹配日志消息"),
    from_time: Optional[datetime] = None,
    to_time: Optional[datetime] = None,
    page: int = Query(1, ge=1, description="分页页码"),
    page_size: int = Query(50, ge=1, le=200, description="单页数量"),
    service: LogService = Depends(get_log_service),
):
    """查询日志列表，支持多条件过滤"""
    try:
        return service.query_logs(
            log_type=type,
            level=level,
            keyword=keyword,
            from_time=from_time,
            to_time=to_time,
            page=page,
            page_size=page_size,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"日志查询失败: {e}")


@router.get("/logs/stream")
def stream_logs():
    """SSE 实时推送日志（预留接口）"""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="SSE 实时日志推送将在后续版本实现"
    )
