"""Embedding service and provider abstractions for vector embedding generation."""

import math
from abc import ABC, abstractmethod

from backend.rag.exceptions import EmbeddingError


class IEmbeddingProvider(ABC):
    """Abstract port interface for embedding provider adapters."""

    @abstractmethod
    async def embed_text(self, text: str) -> list[float]:
        """Generate normalized vector embedding for single text string."""

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate normalized vector embeddings for batch of text strings."""


class MockEmbeddingProvider(IEmbeddingProvider):
    """Mock embedding provider generating 384-dimensional normalized vectors."""

    def __init__(self, dimensions: int = 384) -> None:
        """Initialize mock embedding provider with target vector dimensions.

        Args:
            dimensions: Vector embedding length (default 384).
        """
        self.dimensions = dimensions

    async def embed_text(self, text: str) -> list[float]:
        """Generate 384-dim normalized pseudo-vector based on character frequencies."""
        if not text:
            raw = [0.0] * self.dimensions
            raw[0] = 1.0
            return raw

        vec = [0.0] * self.dimensions
        words = text.lower().split()

        for i, char in enumerate(text.lower()):
            idx = (ord(char) * (i + 1)) % self.dimensions
            vec[idx] += 1.0

        for i, word in enumerate(words):
            hash_val = sum(ord(c) for c in word)
            idx = (hash_val * (i + 3)) % self.dimensions
            vec[idx] += 2.0

        # L2 Normalize
        magnitude = math.sqrt(sum(v * v for v in vec))
        if magnitude == 0:
            return [0.0] * self.dimensions
        return [v / magnitude for v in vec]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate batch embeddings."""
        return [await self.embed_text(t) for t in texts]


class EmbeddingService:
    """Service managing embedding generation via configured provider adapter."""

    def __init__(self, provider: IEmbeddingProvider | None = None) -> None:
        """Initialize EmbeddingService with provider dependency."""
        self._provider = provider or MockEmbeddingProvider()

    async def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding vector for a single text prompt."""
        try:
            return await self._provider.embed_text(text)
        except Exception as exc:
            raise EmbeddingError(f"Embedding generation failed: {exc}") from exc

    async def generate_batch_embeddings(
        self, texts: list[str]
    ) -> list[list[float]]:
        """Generate embedding vectors for a list of text prompts."""
        try:
            return await self._provider.embed_batch(texts)
        except Exception as exc:
            raise EmbeddingError(f"Batch embedding generation failed: {exc}") from exc
