"""Tool Runtime subsystem exception definitions."""

from typing import Any

from backend.core.exceptions import PlatformError


class ToolRuntimeError(PlatformError):
    """Base exception for all Tool Runtime errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "TOOL_RUNTIME_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ToolRuntimeError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
        )


class ToolNotFoundError(ToolRuntimeError):
    """Raised when a requested tool is not registered."""

    def __init__(
        self,
        tool_name: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ToolNotFoundError."""
        super().__init__(
            message=f"Tool '{tool_name}' was not found in ToolRegistry.",
            error_code="TOOL_NOT_FOUND",
            details=details,
        )


class ToolValidationError(ToolRuntimeError):
    """Raised when tool execution parameters fail validation."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ToolValidationError."""
        super().__init__(
            message=message,
            error_code="TOOL_VALIDATION_ERROR",
            details=details,
        )


class ToolExecutionError(ToolRuntimeError):
    """Raised when tool execution raises an unhandled exception."""

    def __init__(
        self,
        tool_name: str,
        reason: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ToolExecutionError."""
        super().__init__(
            message=f"Execution of tool '{tool_name}' failed: {reason}",
            error_code="TOOL_EXECUTION_ERROR",
            details=details,
        )
