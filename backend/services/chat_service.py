"""Application service orchestrating chat execution via Agent Runtime."""

from typing import Any

from backend.agent_runtime import AgentRuntimeService
from backend.core.types import Err, ErrorInfo, Ok, Result
from backend.pipeline import AIRequestPipeline, PipelineRequest, PipelineResponse


class ChatService:
    """Application use-case orchestrator service for chat completion processing."""

    def __init__(
        self,
        pipeline: AIRequestPipeline,
        agent_service: AgentRuntimeService | None = None,
    ) -> None:
        """Initialize ChatService with pipeline and optional AgentRuntimeService.

        Args:
            pipeline: AIRequestPipeline instance.
            agent_service: Optional AgentRuntimeService instance.
        """
        self._pipeline = pipeline
        self._agent_service = agent_service

    async def process_chat(
        self,
        message: str,
        conversation_id: str | None = None,
    ) -> Result[str, ErrorInfo]:
        """Process chat message by delegating orchestration to platform services.

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
        if self._agent_service is not None:
            agent_res = await self._agent_service.execute_agent(
                goal=message,
                conversation_id=conversation_id,
            )
            if agent_res.is_success:
                res = agent_res.unwrap()
                meta: dict[str, Any] = {
                    "sources": res.sources,
                    "tool_results": res.tool_results,
                    "trajectory": res.trajectory,
                }
                return Ok(
                    PipelineResponse(
                        content=res.answer,
                        conversation_id=res.conversation_id,
                        model_used="mock/mock-model",
                        provider_used="mock",
                        tokens_used=20,
                        estimated_cost=0.0,
                        metadata=meta,
                    )
                )

        # Fallback to direct pipeline execution
        request = PipelineRequest(
            prompt=message,
            conversation_id=conversation_id,
        )
        return await self._pipeline.execute(request)
