"""OpenAI LLM Provider adapter implementation stub."""

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


class OpenAILLMProviderAdapter(BaseLLMProviderAdapter):
    """OpenAI LLM provider integration adapter."""

    def __init__(self) -> None:
        """Initialize OpenAI provider metadata specifications."""
        self._models = [
            ModelMetadata(
                model_id=ModelIdentifier(name="gpt-4o", provider="openai"),
                provider_name="openai",
                context_window=128000,
                max_output_tokens=4096,
                capabilities={
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CHAT,
                    ModelCapability.VISION,
                    ModelCapability.FUNCTION_CALLING,
                    ModelCapability.STREAMING,
                    ModelCapability.JSON_OUTPUT,
                },
                input_cost_per_1k_tokens=0.005,
                output_cost_per_1k_tokens=0.015,
            ),
            ModelMetadata(
                model_id=ModelIdentifier(name="gpt-4o-mini", provider="openai"),
                provider_name="openai",
                context_window=128000,
                max_output_tokens=4096,
                capabilities={
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CHAT,
                    ModelCapability.STREAMING,
                },
                input_cost_per_1k_tokens=0.00015,
                output_cost_per_1k_tokens=0.0006,
            ),
        ]

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "openai"

    async def generate_completion(
        self, request: CompletionRequest
    ) -> Result[CompletionResponse, ErrorInfo]:
        """Generate OpenAI completion response stub."""
        response = CompletionResponse(
            id=self._generate_completion_id("openai"),
            model=request.model,
            content="Hello from NeuroFlow AI OpenAI Provider Adapter",
            usage=UsageInfo(
                prompt_tokens=15,
                completion_tokens=10,
                total_tokens=25,
                estimated_cost=0.0002,
            ),
            finish_reason="stop",
            raw_response={"provider": "openai", "status": "mocked"},
        )
        return Ok(response)

    async def generate_stream(
        self, request: CompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        """Yield OpenAI response stream chunk stub."""
        yield StreamChunk(
            id=self._generate_completion_id("openai-stream"),
            model=request.model,
            delta_content="Hello from NeuroFlow AI OpenAI Provider Adapter",
            finish_reason="stop",
        )

    def get_supported_models(self) -> list[ModelMetadata]:
        """Return supported OpenAI models."""
        return self._models
