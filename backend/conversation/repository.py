"""Conversation repository abstract interface port."""

from abc import ABC, abstractmethod

from backend.conversation.conversation import Conversation
from backend.core.value_objects import EntityId, TenantId


class IConversationRepository(ABC):
    """Abstract port interface for conversation aggregate persistence."""

    @abstractmethod
    async def save(self, conversation: Conversation) -> None:
        """Save or update conversation aggregate in storage."""

    @abstractmethod
    async def get_by_id(self, conversation_id: EntityId) -> Conversation | None:
        """Retrieve conversation aggregate by EntityId."""

    @abstractmethod
    async def delete(self, conversation_id: EntityId) -> bool:
        """Delete conversation aggregate by EntityId."""

    @abstractmethod
    async def list_conversations(
        self, tenant_id: TenantId | None = None, limit: int = 50
    ) -> list[Conversation]:
        """List stored conversation aggregates, optionally filtered by TenantId."""


__all__ = [
    "IConversationRepository",
]
