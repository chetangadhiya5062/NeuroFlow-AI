"""Conversation application service for high-level lifecycle management."""

from typing import Any

from backend.conversation.conversation import Conversation
from backend.conversation.exceptions import ConversationError
from backend.conversation.message import Message
from backend.conversation.models import MessageRole
from backend.conversation.repository import IConversationRepository
from backend.core.types import Err, ErrorInfo, Ok, Result
from backend.core.value_objects import EntityId, TenantId


class ConversationService:
    """Service managing conversation creation, retrieval, and message sequence."""

    def __init__(self, repository: IConversationRepository) -> None:
        """Initialize ConversationService with repository dependency.

        Args:
            repository: IConversationRepository interface implementation.
        """
        self._repository = repository

    async def create_conversation(
        self,
        tenant_id: TenantId | None = None,
        title: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Conversation:
        """Create and persist a new conversation aggregate.

        Args:
            tenant_id: Optional TenantId.
            title: Optional conversation title header.
            metadata: Optional metadata dictionary.

        Returns:
            Persisted Conversation instance.
        """
        conversation = Conversation.create(
            tenant_id=tenant_id,
            title=title,
            metadata=metadata,
        )
        await self._repository.save(conversation)
        return conversation

    async def get_conversation(
        self, conversation_id: EntityId | str
    ) -> Result[Conversation, ErrorInfo]:
        """Retrieve conversation aggregate by ID.

        Args:
            conversation_id: EntityId or string ID.

        Returns:
            Result wrapping Conversation or ErrorInfo if not found.
        """
        cid = (
            conversation_id
            if isinstance(conversation_id, EntityId)
            else EntityId(conversation_id)
        )
        conversation = await self._repository.get_by_id(cid)
        if conversation is None:
            return Err(
                ErrorInfo(
                    message=f"Conversation '{cid.value}' was not found.",
                    error_code="CONVERSATION_NOT_FOUND",
                )
            )
        return Ok(conversation)

    async def add_message(
        self,
        conversation_id: EntityId | str,
        role: MessageRole | str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> Result[Message, ErrorInfo]:
        """Append message to conversation and save update.

        Args:
            conversation_id: Target conversation EntityId or string.
            role: MessageRole enum or string.
            content: Message content text string.
            metadata: Optional message metadata.

        Returns:
            Result wrapping appended Message or ErrorInfo.
        """
        res = await self.get_conversation(conversation_id)
        if not res.is_success:
            return Err(res.unwrap_err())

        conversation = res.unwrap()
        try:
            message = conversation.add_message(
                role=role, content=content, metadata=metadata
            )
            await self._repository.save(conversation)
            return Ok(message)
        except ConversationError as exc:
            return Err(
                ErrorInfo(
                    message=exc.message,
                    error_code=exc.error_code,
                    details=exc.details,
                )
            )

    async def get_history(
        self, conversation_id: EntityId | str
    ) -> Result[list[Message], ErrorInfo]:
        """Retrieve message sequence history for conversation.

        Args:
            conversation_id: Target conversation EntityId or string.

        Returns:
            Result wrapping list of Messages or ErrorInfo.
        """
        res = await self.get_conversation(conversation_id)
        if not res.is_success:
            return Err(res.unwrap_err())
        return Ok(res.unwrap().get_history())
