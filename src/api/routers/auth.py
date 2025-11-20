"""
认证路由
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/auth/login")
def login():
    return {"status": "ok"}
