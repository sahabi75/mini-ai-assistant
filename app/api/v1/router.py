"""Aggregates all v1 API routers."""

from fastapi import APIRouter

from app.api.v1.endpoints import chat, health, upload

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(upload.router)
api_router.include_router(chat.router)