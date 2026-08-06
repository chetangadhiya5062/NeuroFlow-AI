"""Platform bootstrap logic for initializing settings, logging, and container."""

import logging

import structlog

from backend.config import (
    PydanticConfigurationProvider,
    ServiceContainer,
    Settings,
    get_container,
    get_settings,
)
from backend.core.ports import IConfigurationProvider


def configure_logging(settings: Settings) -> None:
    """Configure structlog and standard library logging based on settings.

    Args:
        settings: Root platform settings instance.
    """
    log_level = getattr(logging, settings.logging.level.upper(), logging.INFO)

    renderer: structlog.types.Processor
    if settings.logging.format == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def register_foundation_services(
    container: ServiceContainer, settings: Settings
) -> None:
    """Register platform configuration and foundation ports in container.

    Args:
        container: Target ServiceContainer instance.
        settings: Root platform settings instance.
    """
    # Register Configuration Provider
    config_provider = PydanticConfigurationProvider(settings)
    container.register_singleton(
        IConfigurationProvider, instance=config_provider  # type: ignore[type-abstract]
    )


def register_infrastructure_adapters(container: ServiceContainer) -> None:
    """Placeholder hook for future infrastructure adapter registrations.

    Args:
        container: Target ServiceContainer instance.
    """
    # Infrastructure adapters (PostgreSQL, Redis, Qdrant, Neo4j, OpenAI)
    # will be registered here in Milestone 2.
    pass


def register_runtime_engines(container: ServiceContainer) -> None:
    """Placeholder hook for future Layer 3 platform runtime engine registrations.

    Args:
        container: Target ServiceContainer instance.
    """
    # Platform runtimes (Workflow, Agent, Tool, RAG, Prompt, Gateway)
    # will be registered here in Milestone 3-6.
    pass


def bootstrap_platform(
    container: ServiceContainer | None = None,
    settings: Settings | None = None,
) -> tuple[ServiceContainer, Settings]:
    """Bootstrap platform configuration, logging, and dependency container.

    Args:
        container: Optional explicit ServiceContainer instance.
        settings: Optional explicit Settings instance.

    Returns:
        Tuple of (initialized ServiceContainer, active Settings).
    """
    active_settings = settings or get_settings()
    active_container = container or get_container()

    # 1. Configure structured logging
    configure_logging(active_settings)

    # 2. Register foundation services
    register_foundation_services(active_container, active_settings)

    # 3. Register infrastructure adapters (placeholder hook)
    register_infrastructure_adapters(active_container)

    # 4. Register runtime engines (placeholder hook)
    register_runtime_engines(active_container)

    return active_container, active_settings
