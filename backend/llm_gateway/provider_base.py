"""Base LLM provider adapter supplying shared helper logic and contract enforcing."""

from abc import ABC
from collections.abc import AsyncGenerator
from typing import Any
from uuid import uuid4

from backend.core.types import Err, ErrorInfo, Result
from backend.llm_gateway.models import (
    CompletionRequest,
    CompletionResponse,
    ModelMetadata,
    StreamChunk,
)
from backend.llm_gateway.provider import ILLMProviderAdapter


class BaseLLMProviderAdapter(ILLMProviderAdapter, ABC):
    """Base abstract implementation for LLM provider adapters."""

    def _format_error(
        self, message: str, error_code: str, retryable: bool = False
    ) -> Result[Any, ErrorInfo]:
        """Create standardized ErrorInfo error result payload."""
        return Err(
            ErrorInfo(
                message=message,
                error_code=error_code,
                retryable=retryable,
            )
        )

    def _generate_completion_id(self, prefix: str = "comp") -> str:
        """Generate unique completion identifier string."""
        return f"{prefix}-{uuid4()}"

    async def generate_completion(
        self, request: CompletionRequest
    ) -> Result[CompletionResponse, ErrorInfo]:
        """Default completion generation template method."""
        msg = f"Provider '{self.provider_name}' does not implement completion."
        return self._format_error(
            message=msg,
            error_code="PROVIDER_NOT_IMPLEMENTED",
        )

    async def generate_stream(
        self, request: CompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        """Default streaming generation template method."""
        yield StreamChunk(
            id=self._generate_completion_id("stream"),
            model=request.model,
            delta_content=f"Placeholder stream from provider '{self.provider_name}'.",
            finish_reason="stop",
        )

    def get_supported_models(self) -> list[ModelMetadata]:
        """Return list of supported model metadata specifications."""
        return []
