"""Ollama local LLM Provider adapter implementation stub."""

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


class OllamaLLMProviderAdapter(BaseLLMProviderAdapter):
    """Ollama local LLM provider integration adapter."""

    def __init__(self) -> None:
        """Initialize Ollama provider metadata specifications."""
        self._models = [
            ModelMetadata(
                model_id=ModelIdentifier(name="llama3", provider="ollama"),
                provider_name="ollama",
                context_window=8192,
                max_output_tokens=2048,
                capabilities={
                    ModelCapability.TEXT_GENERATION,
                    ModelCapability.CHAT,
                    ModelCapability.STREAMING,
                },
                input_cost_per_1k_tokens=0.0,
                output_cost_per_1k_tokens=0.0,
            )
        ]

    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "ollama"

    async def generate_completion(
        self, request: CompletionRequest
    ) -> Result[CompletionResponse, ErrorInfo]:
        """Generate Ollama completion response stub."""
        response = CompletionResponse(
            id=self._generate_completion_id("ollama"),
            model=request.model,
            content="Hello from NeuroFlow AI Ollama Provider Adapter",
            usage=UsageInfo(
                prompt_tokens=15,
                completion_tokens=10,
                total_tokens=25,
                estimated_cost=0.0,
            ),
            finish_reason="stop",
            raw_response={"provider": "ollama", "status": "mocked"},
        )
        return Ok(response)

    async def generate_stream(
        self, request: CompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        """Yield Ollama response stream chunk stub."""
        yield StreamChunk(
            id=self._generate_completion_id("ollama-stream"),
            model=request.model,
            delta_content="Hello from NeuroFlow AI Ollama Provider Adapter",
            finish_reason="stop",
        )

    def get_supported_models(self) -> list[ModelMetadata]:
        """Return supported Ollama models."""
        return self._models
