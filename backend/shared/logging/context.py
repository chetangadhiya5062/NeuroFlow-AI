"""Context variable management for request tracing and log correlation."""

from contextvars import ContextVar

request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)
correlation_id_var: ContextVar[str | None] = ContextVar(
    "correlation_id", default=None
)
trace_id_var: ContextVar[str | None] = ContextVar("trace_id", default=None)
tenant_id_var: ContextVar[str | None] = ContextVar("tenant_id", default=None)


def set_request_context(
    request_id: str | None = None,
    correlation_id: str | None = None,
    trace_id: str | None = None,
    tenant_id: str | None = None,
) -> None:
    """Set active request context variables for tracing and logging."""
    if request_id is not None:
        request_id_var.set(request_id)
    if correlation_id is not None:
        correlation_id_var.set(correlation_id)
    if trace_id is not None:
        trace_id_var.set(trace_id)
    if tenant_id is not None:
        tenant_id_var.set(tenant_id)


def get_request_context() -> dict[str, str | None]:
    """Retrieve dictionary of active request context variables."""
    return {
        "request_id": request_id_var.get(),
        "correlation_id": correlation_id_var.get(),
        "trace_id": trace_id_var.get(),
        "tenant_id": tenant_id_var.get(),
    }


def clear_request_context() -> None:
    """Reset active request context variables to None."""
    request_id_var.set(None)
    correlation_id_var.set(None)
    trace_id_var.set(None)
    tenant_id_var.set(None)
