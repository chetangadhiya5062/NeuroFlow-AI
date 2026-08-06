"""FastAPI async lifespan context manager for NeuroFlow AI."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from backend.app.bootstrap import bootstrap_platform
from backend.app.shutdown import run_shutdown_tasks
from backend.app.startup import run_startup_tasks

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def platform_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and graceful shutdown lifespan events.

    Args:
        app: Target FastAPI application instance.

    Yields:
        Control to FastAPI runtime while application serves requests.
    """
    logger.info("Initializing NeuroFlow AI application lifespan")

    # 1. Bootstrap platform configuration, logging, and container
    container, settings = bootstrap_platform()

    # 2. Run async startup tasks
    await run_startup_tasks(container, settings)

    # 3. Store container & settings state on application state
    app.state.container = container
    app.state.settings = settings

    try:
        # Yield control to web server
        yield
    finally:
        # 4. Run async graceful shutdown tasks
        logger.info("Tearing down NeuroFlow AI application lifespan")
        await run_shutdown_tasks(container, settings)
