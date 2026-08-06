"""Request logging, timing, and correlation ID propagation middleware."""

import time
from uuid import uuid4

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.shared.logging.context import (
    clear_request_context,
    set_request_context,
)

logger = structlog.get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request timing, correlation ID extraction, and logging."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process incoming request, inject correlation headers, and log duration.

        Args:
            request: Incoming HTTP request.
            call_next: Next request handler in pipeline.

        Returns:
            HTTP Response object with correlation headers attached.
        """
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        correlation_id = request.headers.get("X-Correlation-ID") or request_id
        trace_id = request.headers.get("X-Trace-ID") or str(uuid4())
        tenant_id = request.headers.get("X-Tenant-ID")

        set_request_context(
            request_id=request_id,
            correlation_id=correlation_id,
            trace_id=trace_id,
            tenant_id=tenant_id,
        )

        start_time = time.perf_counter()

        logger.info(
            "HTTP request started",
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else None,
        )

        try:
            response = await call_next(request)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Correlation-ID"] = correlation_id

            logger.info(
                "HTTP request completed",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms,
            )
            return response
        finally:
            clear_request_context()
