"""Application service orchestrating chat execution via AI Request Pipeline."""

from backend.core.types import Err, ErrorInfo, Ok, Result
from backend.pipeline import AIRequestPipeline, PipelineRequest


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
        request = PipelineRequest(
            prompt=message,
            conversation_id=conversation_id,
        )
        result = await self._pipeline.execute(request)
        if result.is_success:
            return Ok(result.unwrap().content)
        return Err(result.unwrap_err())
