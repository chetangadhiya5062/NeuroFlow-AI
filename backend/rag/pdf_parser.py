"""PDF document text extraction parser."""

import io

import pypdf

from backend.rag.exceptions import PDFParsingError


class PDFParser:
    """Extractor parsing raw text content from PDF byte payloads."""

    def parse_pdf(self, content: bytes) -> str:
        """Extract plain text from PDF file bytes.

        Args:
            content: Raw PDF file byte content.

        Returns:
            Extracted text string.

        Raises:
            PDFParsingError: If PDF structure is invalid or corrupt.
        """
        if not content:
            return ""

        try:
            stream = io.BytesIO(content)
            reader = pypdf.PdfReader(stream)
            extracted_pages = []

            for _idx, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    extracted_pages.append(text.strip())

            return "\n\n".join(extracted_pages)
        except Exception as exc:
            raise PDFParsingError(
                f"Failed to parse PDF document content: {exc}"
            ) from exc

    def parse_document(self, content: bytes, file_extension: str) -> str:
        """Extract text content based on file extension.

        Args:
            content: Raw file byte content.
            file_extension: File extension (e.g. '.pdf', '.txt', '.md').

        Returns:
            Extracted plain text string.
        """
        ext = file_extension.lower()
        if ext == ".pdf":
            return self.parse_pdf(content)

        # Fallback to UTF-8 decoding for TXT / Markdown
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content.decode("latin-1", errors="replace")
