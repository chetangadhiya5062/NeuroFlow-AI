"""Document metadata value object definition."""

from dataclasses import dataclass, field
from typing import Any

from backend.core.value_objects import Timestamp


@dataclass(frozen=True)
class DocumentMetadata:
    """Immutable metadata descriptor for an ingested document.

    Attributes:
        filename: Original file name string.
        size_bytes: Document file size in bytes.
        mime_type: Validated MIME content-type string.
        file_extension: File extension string (e.g. '.pdf', '.txt', '.md').
        checksum: Optional SHA-256 hex digest string.
        uploaded_at: Ingestion Timestamp.
        created_at: Creation Timestamp.
        extra: Extensible metadata dictionary.
    """

    filename: str
    size_bytes: int
    mime_type: str
    file_extension: str
    checksum: str | None = None
    uploaded_at: Timestamp = field(default_factory=Timestamp)
    created_at: Timestamp = field(default_factory=Timestamp)
    extra: dict[str, Any] = field(default_factory=dict)
