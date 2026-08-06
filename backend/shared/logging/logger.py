"""Structured logging configuration and logger factory using structlog."""

import logging
import sys
from typing import Any, cast

import structlog
from structlog.types import EventDict, FilteringBoundLogger, Processor

from backend.shared.logging.context import (
    correlation_id_var,
    request_id_var,
    tenant_id_var,
    trace_id_var,
)


def inject_contextvars(
    logger: Any, method_name: str, event_dict: EventDict
) -> EventDict:
    """Inject active context variables into structlog event dictionary."""
    if req_id := request_id_var.get():
        event_dict["request_id"] = req_id
    if corr_id := correlation_id_var.get():
        event_dict["correlation_id"] = corr_id
    if trace_id := trace_id_var.get():
        event_dict["trace_id"] = trace_id
    if tenant_id := tenant_id_var.get():
        event_dict["tenant_id"] = tenant_id
    return event_dict


def configure_structured_logging(
    level: str = "INFO", log_format: str = "json"
) -> None:
    """Configure platform-wide structlog and stdlib logging integration.

    Args:
        level: Logging verbosity level ('DEBUG', 'INFO', 'WARNING', 'ERROR').
        log_format: Output format ('json' or 'console').
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    renderer: Processor
    if log_format.lower() == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        inject_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        renderer,
    ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> FilteringBoundLogger:
    """Get a bound structlog logger instance.

    Args:
        name: Optional module or logger name.

    Returns:
        Bound structlog logger instance.
    """
    return cast(FilteringBoundLogger, structlog.get_logger(name))
