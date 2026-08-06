"""Prompt Runtime subsystem exception definitions."""

from typing import Any

from backend.core.exceptions import PlatformError


class PromptRuntimeError(PlatformError):
    """Base exception for all Prompt Runtime errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "PROMPT_RUNTIME_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize PromptRuntimeError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
        )


class PromptNotFoundError(PromptRuntimeError):
    """Raised when a requested prompt template or version is not registered."""

    def __init__(
        self,
        template_name: str,
        version: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize PromptNotFoundError."""
        ver_str = f" (version '{version}')" if version else ""
        super().__init__(
            message=f"Prompt template '{template_name}'{ver_str} was not found.",
            error_code="PROMPT_NOT_FOUND",
            details=details,
        )


class PromptValidationError(PromptRuntimeError):
    """Raised when a prompt template specification or variable mapping is invalid."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize PromptValidationError."""
        super().__init__(
            message=message,
            error_code="PROMPT_VALIDATION_ERROR",
            details=details,
        )


class PromptRenderError(PromptRuntimeError):
    """Raised when variable substitution or prompt rendering fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize PromptRenderError."""
        super().__init__(
            message=message,
            error_code="PROMPT_RENDER_ERROR",
            details=details,
        )
