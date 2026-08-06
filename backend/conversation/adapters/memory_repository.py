"""In-memory conversation repository adapter implementation."""

import threading

from backend.conversation.conversation import Conversation
from backend.conversation.repository import IConversationRepository
from backend.core.value_objects import EntityId, TenantId


class InMemoryConversationRepository(IConversationRepository):
    """Thread-safe in-memory conversation repository implementation."""

    def __init__(self) -> None:
        """Initialize empty in-memory store and reentrant lock."""
        self._lock = threading.RLock()
        self._store: dict[str, Conversation] = {}

    async def save(self, conversation: Conversation) -> None:
        """Save or update conversation in memory."""
        with self._lock:
            self._store[conversation.id.value] = conversation

    async def get_by_id(self, conversation_id: EntityId) -> Conversation | None:
        """Get conversation from memory by EntityId."""
        with self._lock:
            return self._store.get(conversation_id.value)

    async def delete(self, conversation_id: EntityId) -> bool:
        """Delete conversation from memory by EntityId."""
        with self._lock:
            if conversation_id.value in self._store:
                del self._store[conversation_id.value]
                return True
            return False

    async def list_conversations(
        self, tenant_id: TenantId | None = None, limit: int = 50
    ) -> list[Conversation]:
        """List stored conversations up to specified limit."""
        with self._lock:
            conversations = list(self._store.values())
            if tenant_id is not None:
                conversations = [
                    c for c in conversations if c.tenant_id == tenant_id
                ]
            return conversations[:limit]

    def clear(self) -> None:
        """Clear all stored conversations."""
        with self._lock:
            self._store.clear()
