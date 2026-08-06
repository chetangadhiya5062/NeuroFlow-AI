"""Conversation aggregate root managing message sequence and lifecycle."""

from dataclasses import dataclass, field
from typing import Any

from backend.conversation.exceptions import InvalidMessageError
from backend.conversation.message import Message
from backend.conversation.models import MessageRole
from backend.core.entities import AggregateRoot
from backend.core.value_objects import EntityId, TenantId, Timestamp


@dataclass
class Conversation(AggregateRoot):
    """Conversation aggregate root managing message history and metadata.

    Attributes:
        id: Unique EntityId for conversation.
        tenant_id: Optional multi-tenant TenantId.
        title: Optional conversation title header.
        messages: Mutable list of Message objects.
        metadata: Extensible metadata dictionary.
        created_at: Creation Timestamp.
        updated_at: Last update Timestamp.
    """

    id: EntityId = field(default_factory=EntityId)
    tenant_id: TenantId | None = None
    title: str | None = None
    messages: list[Message] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: Timestamp = field(default_factory=Timestamp)
    updated_at: Timestamp = field(default_factory=Timestamp)

    @classmethod
    def create(
        cls,
        tenant_id: TenantId | None = None,
        title: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "Conversation":
        """Factory creating a new empty Conversation instance.

        Args:
            tenant_id: Optional TenantId.
            title: Optional title string.
            metadata: Optional metadata dictionary.

        Returns:
            New Conversation AggregateRoot.
        """
        now = Timestamp()
        return cls(
            id=EntityId(),
            tenant_id=tenant_id,
            title=title,
            messages=[],
            metadata=metadata or {},
            created_at=now,
            updated_at=now,
        )

    def add_message(
        self,
        role: MessageRole | str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> Message:
        """Append a new message to the conversation sequence.

        Args:
            role: MessageRole enum or string.
            content: Message content text string.
            metadata: Optional message metadata.

        Returns:
            Appended Message object.

        Raises:
            InvalidMessageError: If content is empty or blank.
        """
        if not content or not content.strip():
            raise InvalidMessageError("Message content cannot be empty.")

        message = Message.create(role=role, content=content, metadata=metadata)
        self.messages.append(message)
        self.updated_at = Timestamp()
        return message

    def get_history(self) -> list[Message]:
        """Return shallow copy of conversation message sequence."""
        return list(self.messages)
