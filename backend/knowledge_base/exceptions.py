"""Knowledge Base subsystem exception definitions."""

from typing import Any

from backend.core.exceptions import PlatformError


class KnowledgeBaseError(PlatformError):
    """Base exception for all Knowledge Base subsystem errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "KNOWLEDGE_BASE_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize KnowledgeBaseError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
        )


class DocumentNotFoundError(KnowledgeBaseError):
    """Raised when a requested document entity is not found."""

    def __init__(
        self,
        document_id: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize DocumentNotFoundError."""
        super().__init__(
            message=f"Document '{document_id}' was not found.",
            error_code="DOCUMENT_NOT_FOUND",
            details=details,
        )


class UnsupportedFormatError(KnowledgeBaseError):
    """Raised when an uploaded document file extension or MIME type is unsupported."""

    def __init__(
        self,
        filename: str,
        mime_type: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize UnsupportedFormatError."""
        type_str = f" with content type '{mime_type}'" if mime_type else ""
        super().__init__(
            message=(
                f"File '{filename}'{type_str} is not a supported format. "
                "Supported formats are PDF (.pdf), TXT (.txt), and Markdown (.md)."
            ),
            error_code="UNSUPPORTED_DOCUMENT_FORMAT",
            details=details,
        )


class StorageError(KnowledgeBaseError):
    """Raised when local file I/O operations fail."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize StorageError."""
        super().__init__(
            message=message,
            error_code="STORAGE_ERROR",
            details=details,
        )
