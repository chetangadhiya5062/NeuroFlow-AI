"""Anthropic LLM Provider adapter implementation placeholder."""

from collections.abc import AsyncGenerator

from backend.core.types import ErrorInfo, Ok, Result
from backend.core.value_objects import ModelIdentifier
from backend.llm_gateway.models import (
    CompletionRequest,
    CompletionResponse,
    ModelCapability,
    ModelMetadata,
    StreamChunk,
    UsageInfo,
)
from backend.llm_gateway.provider_base import BaseLLMProviderAdapter


class AnthropicLLMProviderAdapter(BaseLLMProviderAdapter):
    """Anthropic LLM provider integration adapter placeholder."""

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize Anthropic provider metadata specifications.

        Args:
            api_key: Optional Anthropic API Key string.
        """
        self._api_key = api_key
        self._models = [
            ModelMetadata(
                model_id=ModelIdentifier(
                    name="claude-3-5-sonnet-latest", provider="anthropic"
                ),
                provider_name="anthropic",
                context_window=200000,
                max_output_tokens=8192,
                capabilities={
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CHAT,
                    ModelCapability.VISION,
                    ModelCapability.FUNCTION_CALLING,
                    ModelCapability.STREAMING,
                },
                input_cost_per_1k_tokens=0.003,
                output_cost_per_1k_tokens=0.015,
            )
        ]

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "anthropic"

    async def generate_completion(
        self, request: CompletionRequest
    ) -> Result[CompletionResponse, ErrorInfo]:
        """Generate Anthropic completion response stub placeholder."""
        response = CompletionResponse(
            id=self._generate_completion_id("anthropic"),
            model=request.model,
            content="Hello from NeuroFlow AI Anthropic Provider Adapter",
            usage=UsageInfo(
                prompt_tokens=15,
                completion_tokens=10,
                total_tokens=25,
                estimated_cost=0.0002,
            ),
            finish_reason="stop",
            raw_response={"provider": "anthropic", "status": "placeholder"},
        )
        return Ok(response)

    async def generate_stream(
        self, request: CompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        """Yield Anthropic response stream chunk stub placeholder."""
        yield StreamChunk(
            id=self._generate_completion_id("anthropic-stream"),
            model=request.model,
            delta_content="Hello from NeuroFlow AI Anthropic Provider Adapter",
            finish_reason="stop",
        )

    def get_supported_models(self) -> list[ModelMetadata]:
        """Return supported Anthropic models."""
        return self._models
