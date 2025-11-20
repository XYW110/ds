"""
FastAPI 应用入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, strategy, signal, logs, status


def create_app() -> FastAPI:
    app = FastAPI(title="DeepSeek Trading API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"]
    )

    app.include_router(auth.router, prefix="/api")
    app.include_router(strategy.router, prefix="/api")
    app.include_router(signal.router, prefix="/api")
    app.include_router(logs.router, prefix="/api")
    app.include_router(status.router, prefix="/api")

    return app
