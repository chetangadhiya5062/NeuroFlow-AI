"""Document parser and format validation utility."""

from pathlib import Path
from typing import ClassVar

from backend.knowledge_base.exceptions import UnsupportedFormatError


class DocumentParser:
    """Validator inspecting uploaded document formats and MIME types."""

    SUPPORTED_EXTENSIONS: ClassVar[set[str]] = {
        ".pdf",
        ".txt",
        ".md",
        ".markdown",
    }
    MIME_TYPE_MAP: ClassVar[dict[str, str]] = {
        ".pdf": "application/pdf",
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".markdown": "text/markdown",
    }

    def validate_format(
        self, filename: str, content_type: str | None = None
    ) -> tuple[str, str]:
        """Validate filename extension and MIME type.

        Args:
            filename: Name of uploaded file.
            content_type: Optional MIME content-type string.

        Returns:
            Tuple of (file_extension, canonical_mime_type).

        Raises:
            UnsupportedFormatError: If file extension is not supported.
        """
        ext = Path(filename).suffix.lower()
        if not ext or ext not in self.SUPPORTED_EXTENSIONS:
            raise UnsupportedFormatError(
                filename=filename, mime_type=content_type
            )

        mime_type = (
            content_type
            if content_type and "octet-stream" not in content_type
            else self.MIME_TYPE_MAP.get(ext, "application/octet-stream")
        )

        return ext, mime_type
