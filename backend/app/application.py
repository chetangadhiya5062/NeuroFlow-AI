"""FastAPI application factory for NeuroFlow AI."""

from typing import Any

from fastapi import FastAPI

from backend.app.lifespan import platform_lifespan
from backend.config import get_settings


def create_app() -> FastAPI:
    """Construct and configure the NeuroFlow AI FastAPI application instance.

    Returns:
        Configured FastAPI application instance.
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.app.name,
        version=settings.app.version,
        description="Enterprise-grade Modular AI Operating Platform",
        docs_url="/docs" if settings.app.debug else None,
        redoc_url="/redoc" if settings.app.debug else None,
        lifespan=platform_lifespan,
    )

    @app.get("/health", tags=["System"])
    async def health_check() -> dict[str, Any]:
        """System readiness and health check ingress endpoint."""
        return {
            "status": "HEALTHY",
            "app": settings.app.name,
            "version": settings.app.version,
            "environment": settings.app.environment,
        }

    return app
