"""Gemini LLM Provider adapter implementation stub."""

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


class GeminiLLMProviderAdapter(BaseLLMProviderAdapter):
    """Google Gemini LLM provider integration adapter."""

    def __init__(self) -> None:
        """Initialize Gemini provider metadata specifications."""
        self._models = [
            ModelMetadata(
                model_id=ModelIdentifier(name="gemini-1.5-pro", provider="gemini"),
                provider_name="gemini",
                context_window=1000000,
                max_output_tokens=8192,
                capabilities={
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CHAT,
                    ModelCapability.VISION,
                    ModelCapability.STREAMING,
                },
                input_cost_per_1k_tokens=0.00125,
                output_cost_per_1k_tokens=0.005,
            )
        ]

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "gemini"

    async def generate_completion(
        self, request: CompletionRequest
    ) -> Result[CompletionResponse, ErrorInfo]:
        """Generate Gemini completion response stub."""
        response = CompletionResponse(
            id=self._generate_completion_id("gemini"),
            model=request.model,
            content="Hello from NeuroFlow AI Gemini Provider Adapter",
            usage=UsageInfo(
                prompt_tokens=15,
                completion_tokens=10,
                total_tokens=25,
                estimated_cost=0.0001,
            ),
            finish_reason="stop",
            raw_response={"provider": "gemini", "status": "mocked"},
        )
        return Ok(response)

    async def generate_stream(
        self, request: CompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        """Yield Gemini response stream chunk stub."""
        yield StreamChunk(
            id=self._generate_completion_id("gemini-stream"),
            model=request.model,
            delta_content="Hello from NeuroFlow AI Gemini Provider Adapter",
            finish_reason="stop",
        )

    def get_supported_models(self) -> list[ModelMetadata]:
        """Return supported Gemini models."""
        return self._models
