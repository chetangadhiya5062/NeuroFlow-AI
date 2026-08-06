"""Health and version system check endpoints for NeuroFlow AI."""

from typing import Any

from fastapi import APIRouter

from backend.config import get_settings

router = APIRouter(tags=["System"])


@router.get("/health")
async def get_health() -> dict[str, Any]:
    """Check platform health and operational status."""
    settings = get_settings()
    return {
        "status": "HEALTHY",
        "app": settings.app.name,
        "version": settings.app.version,
        "environment": settings.app.environment,
    }


@router.get("/version")
async def get_version() -> dict[str, Any]:
    """Retrieve platform version, build metadata, and environment details."""
    settings = get_settings()
    return {
        "app_name": settings.app.name,
        "version": settings.app.version,
        "environment": settings.app.environment,
        "debug": settings.app.debug,
    }
