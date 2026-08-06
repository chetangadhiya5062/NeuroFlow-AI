"""LLM Gateway subsystem exceptions."""

from typing import Any

from backend.core.exceptions import LLMProviderError


class LLMGatewayError(LLMProviderError):
    """Base exception for all LLM Gateway errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "LLM_GATEWAY_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize LLMGatewayError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            retryable=retryable,
        )


class ModelNotFoundError(LLMGatewayError):
    """Raised when a requested model identifier is not registered."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ModelNotFoundError."""
        super().__init__(
            message=message,
            error_code="MODEL_NOT_FOUND",
            details=details,
            retryable=False,
        )


class ProviderNotFoundError(LLMGatewayError):
    """Raised when no provider adapter is registered for a given provider name."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ProviderNotFoundError."""
        super().__init__(
            message=message,
            error_code="PROVIDER_NOT_FOUND",
            details=details,
            retryable=False,
        )


class ProviderRoutingError(LLMGatewayError):
    """Raised when request routing or provider fallback fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        retryable: bool = True,
    ) -> None:
        """Initialize ProviderRoutingError."""
        super().__init__(
            message=message,
            error_code="PROVIDER_ROUTING_ERROR",
            details=details,
            retryable=retryable,
        )


class ModelCapabilityMismatchError(LLMGatewayError):
    """Raised when a model does not support a required capability."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ModelCapabilityMismatchError."""
        super().__init__(
            message=message,
            error_code="CAPABILITY_MISMATCH",
            details=details,
            retryable=False,
        )
