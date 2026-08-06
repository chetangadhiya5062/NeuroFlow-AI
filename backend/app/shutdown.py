"""Async shutdown tasks execution for NeuroFlow AI platform."""

import structlog

from backend.config import ServiceContainer, Settings

logger = structlog.get_logger(__name__)


async def run_shutdown_tasks(
    container: ServiceContainer, settings: Settings
) -> None:
    """Execute asynchronous graceful shutdown tasks during application teardown.

    Args:
        container: ServiceContainer instance to teardown.
        settings: Active platform Settings instance.
    """
    logger.info("Executing platform shutdown tasks")

    # 1. Stop background workers and task consumers placeholder hook

    # 2. Close infrastructure connections (DB pool, Redis client) placeholder hook

    # 3. Clear container singletons
    container.reset_singletons()

    logger.info("Platform shutdown completed gracefully")
