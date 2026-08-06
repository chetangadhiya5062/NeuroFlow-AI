"""Application service for orchestrating chat execution via LLM Gateway."""

from backend.core.ports import ILLMGateway
from backend.core.types import Err, ErrorInfo, Result
from backend.core.value_objects import ModelIdentifier


class ChatService:
    """Application use-case orchestrator service for chat completion processing."""

    def __init__(self, gateway: ILLMGateway) -> None:
        """Initialize ChatService with LLM Gateway dependency.

        Args:
            gateway: ILLMGateway interface implementation.
        """
        self._gateway = gateway

    async def process_chat(self, message: str) -> Result[str, ErrorInfo]:
        """Process incoming chat message and execute generation via LLM Gateway.

        Args:
            message: User message prompt string.

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

        model = ModelIdentifier(name="mock-model", provider="mock")
        return await self._gateway.generate_text(prompt=message, model=model)
