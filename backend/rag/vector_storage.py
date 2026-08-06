"""Local vector storage adapter with cosine similarity search."""

import math
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class VectorRecord:
    """Immutable record stored inside vector storage.

    Attributes:
        id: Unique record ID string.
        document_id: Parent document EntityId string.
        text: Original chunk text content.
        embedding: Dense float embedding vector.
        metadata: Associated metadata dictionary.
    """

    id: str
    document_id: str
    text: str
    embedding: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SearchResult:
    """Vector similarity search result match.

    Attributes:
        record: Matched VectorRecord.
        score: Cosine similarity score float (0.0 to 1.0).
    """

    record: VectorRecord
    score: float


class IVectorStore(ABC):
    """Abstract port interface for vector storage engines."""

    @abstractmethod
    async def add_records(self, records: list[VectorRecord]) -> None:
        """Add batch of VectorRecords to storage."""

    @abstractmethod
    async def search(
        self, query_embedding: list[float], top_k: int = 5
    ) -> list[SearchResult]:
        """Search vector store for top_k records nearest to query_embedding."""

    @abstractmethod
    async def delete_by_document_id(self, document_id: str) -> bool:
        """Delete all stored records associated with document_id."""


class LocalVectorStorage(IVectorStore):
    """Thread-safe in-memory vector storage computing exact Cosine Similarity."""

    def __init__(self) -> None:
        """Initialize vector store container and reentrant lock."""
        self._lock = threading.RLock()
        self._records: list[VectorRecord] = []

    def _cosine_similarity(self, vec_a: list[float], vec_b: list[float]) -> float:
        """Compute cosine similarity score between two float vectors."""
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b, strict=False))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    async def add_records(self, records: list[VectorRecord]) -> None:
        """Store records in memory."""
        with self._lock:
            self._records.extend(records)

    async def search(
        self, query_embedding: list[float], top_k: int = 5
    ) -> list[SearchResult]:
        """Compute cosine similarity scores against all records and return top_k."""
        with self._lock:
            results: list[SearchResult] = []
            for record in self._records:
                score = self._cosine_similarity(query_embedding, record.embedding)
                results.append(SearchResult(record=record, score=score))

            # Sort descending by similarity score
            results.sort(key=lambda r: r.score, reverse=True)
            return results[:top_k]

    async def delete_by_document_id(self, document_id: str) -> bool:
        """Remove records associated with document_id."""
        with self._lock:
            initial_count = len(self._records)
            self._records = [
                r for r in self._records if r.document_id != document_id
            ]
            return len(self._records) < initial_count

    def clear(self) -> None:
        """Clear vector storage."""
        with self._lock:
            self._records.clear()
