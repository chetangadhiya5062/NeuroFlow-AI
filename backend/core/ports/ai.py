"""Abstract port contracts for AI memory, knowledge, vectors, and LLM gateway."""

from abc import ABC, abstractmethod
from typing import Any

from backend.core.types import ErrorInfo, Result
from backend.core.value_objects import (
    EntityId,
    ModelIdentifier,
    TenantId,
    TokenBudget,
)


class IMemoryStore(ABC):
    """Abstract port interface for AI Memory Layer persistence adapters."""

    @abstractmethod
    async def save_memory(
        self, tenant_id: TenantId, key: str, value: dict[str, Any]
    ) -> Result[bool, ErrorInfo]:
        """Persist memory payload key-value pair for tenant."""

    @abstractmethod
    async def read_memory(
        self, tenant_id: TenantId, key: str
    ) -> Result[dict[str, Any] | None, ErrorInfo]:
        """Read memory payload key-value pair for tenant."""

    @abstractmethod
    async def delete_memory(
        self, tenant_id: TenantId, key: str
    ) -> Result[bool, ErrorInfo]:
        """Delete memory entry by key for tenant."""


class IKnowledgeStore(ABC):
    """Abstract port interface for Knowledge Base document repositories."""

    @abstractmethod
    async def store_document(
        self,
        tenant_id: TenantId,
        document_id: EntityId,
        content: str,
        metadata: dict[str, Any],
    ) -> Result[EntityId, ErrorInfo]:
        """Store knowledge document content and metadata."""

    @abstractmethod
    async def get_document(
        self, tenant_id: TenantId, document_id: EntityId
    ) -> Result[dict[str, Any] | None, ErrorInfo]:
        """Retrieve knowledge document by ID for tenant."""


class IKnowledgeGraphStore(ABC):
    """Abstract port interface for Knowledge Graph stores (e.g. Neo4j)."""

    @abstractmethod
    async def add_node(
        self,
        tenant_id: TenantId,
        node_id: str,
        label: str,
        properties: dict[str, Any],
    ) -> Result[bool, ErrorInfo]:
        """Create graph node with label and properties."""

    @abstractmethod
    async def add_edge(
        self,
        tenant_id: TenantId,
        source_id: str,
        target_id: str,
        relation: str,
        properties: dict[str, Any],
    ) -> Result[bool, ErrorInfo]:
        """Create directed relationship edge between nodes."""

    @abstractmethod
    async def query_paths(
        self, tenant_id: TenantId, query: str
    ) -> Result[list[dict[str, Any]], ErrorInfo]:
        """Execute graph query and return matching path structures."""


class IVectorStore(ABC):
    """Abstract port interface for vector database adapters (e.g. Qdrant)."""

    @abstractmethod
    async def upsert_vectors(
        self,
        tenant_id: TenantId,
        collection: str,
        vectors: list[list[float]],
        payloads: list[dict[str, Any]],
        ids: list[str],
    ) -> Result[bool, ErrorInfo]:
        """Upsert batch of vectors with payload metadata into collection."""

    @abstractmethod
    async def search_vectors(
        self,
        tenant_id: TenantId,
        collection: str,
        query_vector: list[float],
        top_k: int = 10,
    ) -> Result[list[dict[str, Any]], ErrorInfo]:
        """Execute vector similarity search returning top-k matches."""


class IEmbeddingProvider(ABC):
    """Abstract port interface for text embedding providers."""

    @abstractmethod
    async def embed_text(self, text: str) -> Result[list[float], ErrorInfo]:
        """Generate embedding vector for a single text string."""

    @abstractmethod
    async def embed_batch(
        self, texts: list[str]
    ) -> Result[list[list[float]], ErrorInfo]:
        """Generate embedding vectors for a batch of text strings."""


class ILLMGateway(ABC):
    """Abstract port interface for model routing and LLM generation."""

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        model: ModelIdentifier | None = None,
        budget: TokenBudget | None = None,
    ) -> Result[str, ErrorInfo]:
        """Generate text response using specified model provider."""

    @abstractmethod
    async def generate_chat(
        self,
        messages: list[dict[str, str]],
        model: ModelIdentifier | None = None,
    ) -> Result[dict[str, Any], ErrorInfo]:
        """Generate multi-turn chat completion response."""
