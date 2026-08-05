"""Base platform exception class for NeuroFlow AI."""

from typing import Any


class PlatformError(Exception):
    """Base exception class for all custom errors in NeuroFlow AI.

    All domain, runtime, infrastructure, and application exceptions inherit
    from this class to ensure consistent error metadata and classification.

    Attributes:
        message: Human-readable error message explaining the failure.
        error_code: Canonical uppercase error identifier string.
        details: Optional dictionary containing context metadata.
        retryable: Indicates if the operation may be safely retried.
    """

    def __init__(
        self,
        message: str,
        error_code: str = "PLATFORM_ERROR",
        details: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        """Initialize the base platform error.

        Args:
            message: Explanation of the error condition.
            error_code: Unique uppercase error identifier.
            details: Optional context details dictionary.
            retryable: Whether the failed operation is retryable.
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.retryable = retryable

    def __str__(self) -> str:
        """Return formatted string representation of the exception."""
        if self.details:
            return f"[{self.error_code}] {self.message} (details={self.details})"
        return f"[{self.error_code}] {self.message}"

    def __repr__(self) -> str:
        """Return official representation of the exception instance."""
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"error_code={self.error_code!r}, "
            f"details={self.details!r}, "
            f"retryable={self.retryable!r})"
        )
