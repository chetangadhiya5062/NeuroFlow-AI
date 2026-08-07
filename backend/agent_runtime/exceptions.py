"""Agent Runtime subsystem exception definitions."""

from typing import Any

from backend.core.exceptions import PlatformError


class AgentError(PlatformError):
    """Base exception for all Agent Runtime errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "AGENT_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize AgentError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
        )


class AgentExecutionError(AgentError):
    """Raised when agent reasoning loop execution fails."""

    def __init__(
        self,
        reason: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize AgentExecutionError."""
        super().__init__(
            message=f"Agent execution failed: {reason}",
            error_code="AGENT_EXECUTION_ERROR",
            details=details,
        )


class ActionExecutionError(AgentError):
    """Raised when a specific agent action fails."""

    def __init__(
        self,
        action_name: str,
        reason: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ActionExecutionError."""
        super().__init__(
            message=f"Action '{action_name}' execution failed: {reason}",
            error_code="ACTION_EXECUTION_ERROR",
            details=details,
        )
