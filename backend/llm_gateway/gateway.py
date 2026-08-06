"""Primary LLM Gateway platform subsystem implementing Layer 0 ILLMGateway port."""

from collections.abc import AsyncGenerator
from typing import Any

from backend.core.ports import ILLMGateway
from backend.core.types import Err, ErrorInfo, Ok, Result
from backend.core.value_objects import ModelIdentifier, TokenBudget
from backend.llm_gateway.exceptions import LLMGatewayError
from backend.llm_gateway.models import (
    ChatMessage,
    CompletionRequest,
    CompletionResponse,
    StreamChunk,
    UsageInfo,
)
from backend.llm_gateway.registry import ModelRegistry
from backend.llm_gateway.router import LLMRouter


class LLMGatewayService(ILLMGateway):
    """LLM Gateway subsystem service implementing ILLMGateway port contract."""

    def __init__(
        self,
        router: LLMRouter | None = None,
        registry: ModelRegistry | None = None,
    ) -> None:
        """Initialize LLMGatewayService with registry and router.

        Args:
            router: Optional explicit LLMRouter.
            registry: Optional explicit ModelRegistry.
        """
        self.registry = registry or ModelRegistry()
        self.router = router or LLMRouter(registry=self.registry)

    def calculate_cost(
        self,
        model_id: ModelIdentifier,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> float:
        """Calculate estimated USD cost for token consumption based on model rates.

        Args:
            model_id: Target ModelIdentifier.
            prompt_tokens: Number of prompt tokens.
            completion_tokens: Number of generated completion tokens.

        Returns:
            Calculated cost in USD.
        """
        try:
            metadata = self.registry.get_model(model_id)
            input_cost = (prompt_tokens / 1000.0) * metadata.input_cost_per_1k_tokens
            output_cost = (
                completion_tokens / 1000.0
            ) * metadata.output_cost_per_1k_tokens
            return round(input_cost + output_cost, 6)
        except Exception:
            return 0.0

    async def generate_completion(
        self, request: CompletionRequest
    ) -> Result[CompletionResponse, ErrorInfo]:
        """Execute text or chat completion via routed provider adapter.

        Args:
            request: CompletionRequest payload.

        Returns:
            Result wrapping CompletionResponse or ErrorInfo.
        """
        try:
            adapter = self.router.route_request(request)
            result = await adapter.generate_completion(request)
            if result.is_success:
                res = result.unwrap()
                # Recalculate cost if estimated_cost is 0.0
                if res.usage.estimated_cost == 0.0:
                    cost = self.calculate_cost(
                        res.model,
                        res.usage.prompt_tokens,
                        res.usage.completion_tokens,
                    )
                    updated_usage = UsageInfo(
                        prompt_tokens=res.usage.prompt_tokens,
                        completion_tokens=res.usage.completion_tokens,
                        total_tokens=res.usage.total_tokens,
                        estimated_cost=cost,
                    )
                    res = CompletionResponse(
                        id=res.id,
                        model=res.model,
                        content=res.content,
                        usage=updated_usage,
                        finish_reason=res.finish_reason,
                        raw_response=res.raw_response,
                    )
                return Ok(res)
            return result
        except LLMGatewayError as exc:
            return Err(
                ErrorInfo(
                    message=exc.message,
                    error_code=exc.error_code,
                    details=exc.details,
                    retryable=exc.retryable,
                )
            )
        except Exception as exc:
            return Err(
                ErrorInfo(
                    message=f"Unexpected error in LLM Gateway: {exc}",
                    error_code="GATEWAY_UNEXPECTED_ERROR",
                    retryable=False,
                )
            )

    async def generate_stream(
        self, request: CompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        """Execute streaming completion yielding StreamChunk deltas.

        Args:
            request: CompletionRequest payload (stream=True).

        Yields:
            StreamChunk deltas.
        """
        adapter = self.router.route_request(request)
        async for chunk in adapter.generate_stream(request):
            yield chunk

    # ILLMGateway Port Method Implementations

    async def generate_text(
        self,
        prompt: str,
        model: ModelIdentifier | None = None,
        budget: TokenBudget | None = None,
    ) -> Result[str, ErrorInfo]:
        """Generate text response using specified model provider.

        Args:
            prompt: Text prompt string.
            model: Optional target ModelIdentifier.
            budget: Optional TokenBudget constraint.

        Returns:
            Result wrapping generated text response string or ErrorInfo.
        """
        target_model = model or ModelIdentifier(name="gpt-4o", provider="openai")
        max_tokens = budget.remaining if budget else None

        request = CompletionRequest(
            messages=[ChatMessage(role="user", content=prompt)],
            model=target_model,
            max_tokens=max_tokens,
        )

        res = await self.generate_completion(request)
        if res.is_success:
            return Ok(res.unwrap().content)
        return Err(res.unwrap_err())

    async def generate_chat(
        self,
        messages: list[dict[str, str]],
        model: ModelIdentifier | None = None,
    ) -> Result[dict[str, Any], ErrorInfo]:
        """Generate multi-turn chat completion response.

        Args:
            messages: List of message dictionaries containing 'role' and 'content'.
            model: Optional target ModelIdentifier.

        Returns:
            Result wrapping chat response dictionary or ErrorInfo.
        """
        target_model = model or ModelIdentifier(name="gpt-4o", provider="openai")
        chat_messages = [
            ChatMessage(
                role=msg.get("role", "user"),
                content=msg.get("content", ""),
                name=msg.get("name"),
            )
            for msg in messages
        ]

        request = CompletionRequest(
            messages=chat_messages,
            model=target_model,
        )

        res = await self.generate_completion(request)
        if res.is_success:
            comp = res.unwrap()
            return Ok(
                {
                    "id": comp.id,
                    "model": comp.model.canonical_name,
                    "content": comp.content,
                    "role": "assistant",
                    "usage": {
                        "prompt_tokens": comp.usage.prompt_tokens,
                        "completion_tokens": comp.usage.completion_tokens,
                        "total_tokens": comp.usage.total_tokens,
                        "estimated_cost": comp.usage.estimated_cost,
                    },
                }
            )
        return Err(res.unwrap_err())
