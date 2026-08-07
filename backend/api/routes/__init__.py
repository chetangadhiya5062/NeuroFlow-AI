"""API route registration module for NeuroFlow AI."""

from fastapi import APIRouter

from backend.api.routes.chat import router as chat_router
from backend.api.routes.documents import router as documents_router
from backend.api.routes.health import router as health_router
from backend.api.routes.platform import router as platform_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(chat_router)
api_router.include_router(documents_router)
api_router.include_router(platform_router)

__all__ = [
    "api_router",
    "chat_router",
    "documents_router",
    "health_router",
    "platform_router",
]
