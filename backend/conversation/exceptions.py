"""Conversation subsystem exception definitions."""

from typing import Any

from backend.core.exceptions import PlatformError


class ConversationError(PlatformError):
    """Base exception for all Conversation subsystem errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "CONVERSATION_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ConversationError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
        )


class ConversationNotFoundError(ConversationError):
    """Raised when a requested conversation entity is not found."""

    def __init__(
        self,
        conversation_id: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ConversationNotFoundError."""
        super().__init__(
            message=f"Conversation '{conversation_id}' was not found.",
            error_code="CONVERSATION_NOT_FOUND",
            details=details,
        )


class InvalidMessageError(ConversationError):
    """Raised when a conversation message payload is invalid."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize InvalidMessageError."""
        super().__init__(
            message=message,
            error_code="INVALID_MESSAGE",
            details=details,
        )
