"""Application service orchestrating chat execution via AI Request Pipeline."""

from backend.core.types import Err, ErrorInfo, Ok, Result
from backend.pipeline import AIRequestPipeline, PipelineRequest, PipelineResponse


class ChatService:
    """Application use-case orchestrator service for chat completion processing."""

    def __init__(self, pipeline: AIRequestPipeline) -> None:
        """Initialize ChatService with AIRequestPipeline dependency.

        Args:
            pipeline: AIRequestPipeline instance.
        """
        self._pipeline = pipeline

    async def process_chat(
        self,
        message: str,
        conversation_id: str | None = None,
    ) -> Result[str, ErrorInfo]:
        """Process chat message by delegating orchestration to AIRequestPipeline.

        Args:
            message: User message prompt string.
            conversation_id: Optional target conversation ID string.

        Returns:
            Result wrapping LLM text response string or ErrorInfo.
        """
        res = await self.process_chat_full(
            message=message, conversation_id=conversation_id
        )
        if res.is_success:
            return Ok(res.unwrap().content)
        return Err(res.unwrap_err())

    async def process_chat_full(
        self,
        message: str,
        conversation_id: str | None = None,
    ) -> Result[PipelineResponse, ErrorInfo]:
        """Process chat message returning complete PipelineResponse payload.

        Args:
            message: User message prompt string.
            conversation_id: Optional target conversation ID string.

        Returns:
            Result wrapping PipelineResponse object or ErrorInfo.
        """
        request = PipelineRequest(
            prompt=message,
            conversation_id=conversation_id,
        )
        return await self._pipeline.execute(request)
