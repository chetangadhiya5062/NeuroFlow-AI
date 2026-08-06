"""Exception logging middleware for capturing unhandled request errors."""

from typing import Any

import structlog
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = structlog.get_logger(__name__)


class ExceptionLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware catching unhandled exceptions and logging structured stack traces."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> JSONResponse | Any:
        """Intercept request execution and log unhandled exceptions.

        Args:
            request: Incoming HTTP request.
            call_next: Next request handler in pipeline.

        Returns:
            Response object or 500 JSONResponse if unhandled exception occurs.
        """
        try:
            return await call_next(request)
        except Exception as exc:
            logger.error(
                "Unhandled application exception",
                method=request.method,
                path=request.url.path,
                exception=str(exc),
                exc_info=True,
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error_code": "INTERNAL_SERVER_ERROR",
                    "message": "An unhandled server error occurred.",
                },
            )
