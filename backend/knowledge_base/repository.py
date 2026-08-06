"""Knowledge Base repository interface and in-memory implementation."""

import threading
from abc import ABC, abstractmethod

from backend.core.value_objects import EntityId, TenantId
from backend.knowledge_base.document import Document


class IKnowledgeBaseRepository(ABC):
    """Abstract port interface for Document aggregate metadata persistence."""

    @abstractmethod
    async def save(self, document: Document) -> None:
        """Save or update document aggregate in storage."""

    @abstractmethod
    async def get_by_id(self, document_id: EntityId) -> Document | None:
        """Retrieve document aggregate by EntityId."""

    @abstractmethod
    async def delete(self, document_id: EntityId) -> bool:
        """Delete document aggregate by EntityId."""

    @abstractmethod
    async def list_documents(
        self, tenant_id: TenantId | None = None, limit: int = 50
    ) -> list[Document]:
        """List stored document aggregates, optionally filtered by TenantId."""


class InMemoryKnowledgeBaseRepository(IKnowledgeBaseRepository):
    """Thread-safe in-memory repository implementation for document metadata."""

    def __init__(self) -> None:
        """Initialize empty in-memory store and reentrant lock."""
        self._lock = threading.RLock()
        self._store: dict[str, Document] = {}

    async def save(self, document: Document) -> None:
        """Save document metadata in memory."""
        with self._lock:
            self._store[document.id.value] = document

    async def get_by_id(self, document_id: EntityId) -> Document | None:
        """Get document from memory by EntityId."""
        with self._lock:
            return self._store.get(document_id.value)

    async def delete(self, document_id: EntityId) -> bool:
        """Delete document from memory by EntityId."""
        with self._lock:
            if document_id.value in self._store:
                del self._store[document_id.value]
                return True
            return False

    async def list_documents(
        self, tenant_id: TenantId | None = None, limit: int = 50
    ) -> list[Document]:
        """List stored documents up to specified limit."""
        with self._lock:
            docs = list(self._store.values())
            if tenant_id is not None:
                docs = [d for d in docs if d.tenant_id == tenant_id]
            return docs[:limit]

    def clear(self) -> None:
        """Clear all stored documents."""
        with self._lock:
            self._store.clear()
