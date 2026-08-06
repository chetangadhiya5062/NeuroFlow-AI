"""RAG subsystem exception definitions."""

from typing import Any

from backend.core.exceptions import PlatformError


class RAGError(PlatformError):
    """Base exception for all RAG subsystem errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "RAG_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize RAGError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
        )


class PDFParsingError(RAGError):
    """Raised when PDF file text extraction fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize PDFParsingError."""
        super().__init__(
            message=message,
            error_code="PDF_PARSING_ERROR",
            details=details,
        )


class EmbeddingError(RAGError):
    """Raised when text embedding generation fails."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize EmbeddingError."""
        super().__init__(
            message=message,
            error_code="EMBEDDING_ERROR",
            details=details,
        )


class VectorStorageError(RAGError):
    """Raised when vector index storage or search operations fail."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize VectorStorageError."""
        super().__init__(
            message=message,
            error_code="VECTOR_STORAGE_ERROR",
            details=details,
        )
