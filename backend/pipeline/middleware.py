"""Pipeline middleware interceptors for cross-cutting logging and metrics."""

import time
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable

import structlog

from backend.pipeline.context import PipelineContext

logger = structlog.get_logger(__name__)


class IPipelineMiddleware(ABC):
    """Abstract contract for pipeline middleware interceptors."""

    @abstractmethod
    async def execute(
        self,
        context: PipelineContext,
        next_stage: Callable[[], Awaitable[None]],
    ) -> None:
        """Execute middleware wrapper logic around next pipeline stage.

        Args:
            context: Mutable PipelineContext object.
            next_stage: Callable executing next stage processor.
        """


class LoggingPipelineMiddleware(IPipelineMiddleware):
    """Middleware for measuring stage timing and logging execution events."""

    async def execute(
        self,
        context: PipelineContext,
        next_stage: Callable[[], Awaitable[None]],
    ) -> None:
        """Measure stage execution duration and log completion."""
        start_time = time.perf_counter()
        await next_stage()
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.debug(
            "Pipeline stage completed",
            duration_ms=duration_ms,
        )
