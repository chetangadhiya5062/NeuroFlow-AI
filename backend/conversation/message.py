"""Message entity model for representing individual conversation utterances."""

from dataclasses import dataclass, field
from typing import Any

from backend.conversation.models import MessageRole
from backend.core.value_objects import EntityId, Timestamp


@dataclass(frozen=True)
class Message:
    """Immutable representation of a single conversation message.

    Attributes:
        id: Unique EntityId for message.
        role: MessageRole enum classification.
        content: Text content of message.
        created_at: Creation Timestamp.
        metadata: Extensible metadata dictionary.
    """

    id: EntityId
    role: MessageRole
    content: str
    created_at: Timestamp = field(default_factory=Timestamp)
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        role: MessageRole | str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> "Message":
        """Factory method constructing a new Message.

        Args:
            role: MessageRole enum or string ('user', 'assistant').
            content: Message content text string.
            metadata: Optional metadata dictionary.

        Returns:
            Instantiated immutable Message object.
        """
        role_enum = role if isinstance(role, MessageRole) else MessageRole(role)
        return Message(
            id=EntityId(),
            role=role_enum,
            content=content,
            metadata=metadata or {},
        )
