"""Abstract provider adapter interface for LLM integrations."""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from backend.core.types import ErrorInfo, Result
from backend.llm_gateway.models import (
    CompletionRequest,
    CompletionResponse,
    ModelMetadata,
    StreamChunk,
)


class ILLMProviderAdapter(ABC):
    """Abstract interface contract for LLM provider integration adapters."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the unique provider adapter name (e.g. 'openai', 'anthropic')."""

    @abstractmethod
    async def generate_completion(
        self, request: CompletionRequest
    ) -> Result[CompletionResponse, ErrorInfo]:
        """Execute text or chat completion against provider API."""

    @abstractmethod
    def generate_stream(
        self, request: CompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        """Execute streaming completion yielding StreamChunk deltas."""

    @abstractmethod
    def get_supported_models(self) -> list[ModelMetadata]:
        """Return list of model metadata specifications supported by provider."""
