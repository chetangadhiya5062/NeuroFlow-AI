"""Document text chunker implementation."""

from dataclasses import dataclass, field
from typing import Any

from backend.core.value_objects import EntityId


@dataclass(frozen=True)
class DocumentChunk:
    """Immutable data structure representing a text chunk from a document.

    Attributes:
        id: Unique EntityId for chunk.
        document_id: Source document EntityId string.
        text: Chunk text content.
        index: Sequential chunk index within document.
        metadata: Associated chunk metadata dictionary.
    """

    id: EntityId
    document_id: str
    text: str
    index: int
    metadata: dict[str, Any] = field(default_factory=dict)


class TextChunker:
    """Recursive sliding-window text chunker for RAG document processing."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100) -> None:
        """Initialize TextChunker with target size and overlap bounds.

        Args:
            chunk_size: Maximum character length per chunk.
            chunk_overlap: Overlap character count between consecutive chunks.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(
        self,
        document_id: str,
        text: str,
        extra_metadata: dict[str, Any] | None = None,
    ) -> list[DocumentChunk]:
        """Split document text into a sequence of DocumentChunks.

        Args:
            document_id: Source document EntityId string.
            text: Raw document text string.
            extra_metadata: Optional metadata dictionary to attach to chunks.

        Returns:
            List of DocumentChunk instances.
        """
        if not text or not text.strip():
            return []

        clean_text = text.strip()
        chunks: list[DocumentChunk] = []
        start = 0
        text_len = len(clean_text)
        chunk_idx = 0

        while start < text_len:
            end = start + self.chunk_size
            chunk_str = clean_text[start:end]

            # Adjust end to avoid splitting words if possible
            if end < text_len:
                last_space = chunk_str.rfind(" ")
                if last_space > self.chunk_size // 2:
                    end = start + last_space
                    chunk_str = clean_text[start:end]

            chunk_str = chunk_str.strip()
            if chunk_str:
                meta = dict(extra_metadata or {})
                meta["start_char"] = start
                meta["end_char"] = end
                chunks.append(
                    DocumentChunk(
                        id=EntityId(),
                        document_id=document_id,
                        text=chunk_str,
                        index=chunk_idx,
                        metadata=meta,
                    )
                )
                chunk_idx += 1

            start += self.chunk_size - self.chunk_overlap

        return chunks
