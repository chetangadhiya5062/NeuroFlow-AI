"""FastAPI entry point and application initialization for NeuroFlow AI."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.api.routes import api_router
from backend.app import platform_lifespan
from backend.config import get_settings
from backend.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    PlatformError,
    ValidationError,
)


def get_application() -> FastAPI:
    """Construct and configure the main FastAPI web application instance.

    Returns:
        Configured FastAPI application instance ready for execution.
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

    # Register API routers
    app.include_router(api_router)

    # Register global PlatformError exception handler
    @app.exception_handler(PlatformError)
    async def platform_exception_handler(
        request: Request, exc: PlatformError
    ) -> JSONResponse:
        """Handle custom platform exceptions and convert to standardized JSON errors."""
        status_code = 500
        if isinstance(exc, ValidationError):
            status_code = 400
        elif isinstance(exc, AuthenticationError):
            status_code = 401
        elif isinstance(exc, AuthorizationError):
            status_code = 403
        elif isinstance(exc, NotFoundError):
            status_code = 404

        return JSONResponse(
            status_code=status_code,
            content={
                "error_code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
                "retryable": exc.retryable,
            },
        )

    return app


# Root FastAPI application instance for Uvicorn execution
app = get_application()
