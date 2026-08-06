"""Application service orchestrating chat execution via LLM Gateway and Conversation."""

from backend.conversation import ConversationService, MessageRole
from backend.core.ports import ILLMGateway
from backend.core.types import Err, ErrorInfo, Result
from backend.core.value_objects import ModelIdentifier


class ChatService:
    """Application use-case orchestrator service for chat completion processing."""

    def __init__(
        self,
        gateway: ILLMGateway,
        conversation_service: ConversationService | None = None,
    ) -> None:
        """Initialize ChatService with LLM Gateway and ConversationService dependencies.

        Args:
            gateway: ILLMGateway interface implementation.
            conversation_service: Optional ConversationService instance.
        """
        self._gateway = gateway
        self._conversation_service = conversation_service

    async def process_chat(
        self,
        message: str,
        conversation_id: str | None = None,
    ) -> Result[str, ErrorInfo]:
        """Process chat message, record history in conversation, and generate response.

        Args:
            message: User message prompt string.
            conversation_id: Optional target conversation ID string.

        Returns:
            Result wrapping LLM text response string or ErrorInfo.
        """
        if not message or not message.strip():
            return Err(
                ErrorInfo(
                    message="Chat message prompt cannot be empty.",
                    error_code="VALIDATION_ERROR",
                )
            )

        # 1. Manage Conversation sequence if ConversationService is active
        conv = None
        if self._conversation_service is not None:
            if conversation_id:
                get_res = await self._conversation_service.get_conversation(
                    conversation_id
                )
                if get_res.is_success:
                    conv = get_res.unwrap()
                else:
                    conv = await self._conversation_service.create_conversation(
                        title="Chat Session"
                    )
            else:
                conv = await self._conversation_service.create_conversation(
                    title="Chat Session"
                )

            # Append user message
            await self._conversation_service.add_message(
                conversation_id=conv.id,
                role=MessageRole.USER,
                content=message,
            )

        # 2. Execute generation via LLM Gateway
        model = ModelIdentifier(name="mock-model", provider="mock")
        llm_result = await self._gateway.generate_text(prompt=message, model=model)

        if not llm_result.is_success:
            return llm_result

        response_text = llm_result.unwrap()

        # 3. Append assistant response message to conversation
        if self._conversation_service is not None and conv is not None:
            await self._conversation_service.add_message(
                conversation_id=conv.id,
                role=MessageRole.ASSISTANT,
                content=response_text,
            )

        return llm_result
