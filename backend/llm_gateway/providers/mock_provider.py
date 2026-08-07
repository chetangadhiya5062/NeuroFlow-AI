"""Mock LLM Provider adapter for vertical slice validation and offline testing."""

import re
from collections.abc import AsyncGenerator
from uuid import uuid4

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
from backend.llm_gateway.provider import ILLMProviderAdapter


class MockLLMProviderAdapter(ILLMProviderAdapter):
    """Mock LLM provider adapter returning deterministic responses for testing."""

    def __init__(self, response_text: str | None = None) -> None:
        """Initialize mock provider with optional custom response text.

        Args:
            response_text: Custom text to return in completion responses.
        """
        self._response_text = response_text
        self._mock_model = ModelMetadata(
            model_id=ModelIdentifier(name="mock-model", provider="mock"),
            provider_name="mock",
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

    @property
    def provider_name(self) -> str:
        """Return the unique provider name."""
        return "mock"

    async def generate_completion(
        self, request: CompletionRequest
    ) -> Result[CompletionResponse, ErrorInfo]:
        """Generate mock completion response.

        Args:
            request: CompletionRequest payload.

        Returns:
            Result wrapping mock CompletionResponse.
        """
        prompt_content = (
            request.messages[-1].content if request.messages else ""
        )

        content = self._response_text or "Hello from NeuroFlow AI Mock Provider"

        # Check if prompt contains Tool Result / Execution Result injection
        if "Tool" in prompt_content and "Result" in prompt_content:
            match = re.search(r"Result[^\:]*:\s*([^\n]+)", prompt_content)
            if match:
                val = match.group(1).strip()
                # Format numeric output nicely if possible
                try:
                    num_val = int(val) if val.isdigit() else float(val)
                    formatted_val = (
                        f"{num_val:,}"
                        if isinstance(num_val, int)
                        else str(num_val)
                    )
                except ValueError:
                    formatted_val = val
                content = f"The calculated result is {formatted_val}."

        response = CompletionResponse(
            id=f"mock-{uuid4()}",
            model=request.model,
            content=content,
            usage=UsageInfo(
                prompt_tokens=10,
                completion_tokens=10,
                total_tokens=20,
                estimated_cost=0.0,
            ),
            finish_reason="stop",
            raw_response={"provider": "mock", "status": "success"},
        )
        return Ok(response)

    async def generate_stream(
        self, request: CompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        """Yield single mock stream chunk."""
        content = self._response_text or "Hello from NeuroFlow AI Mock Provider"
        yield StreamChunk(
            id=f"mock-stream-{uuid4()}",
            model=request.model,
            delta_content=content,
            finish_reason="stop",
        )

    def get_supported_models(self) -> list[ModelMetadata]:
        """Return list of supported mock model metadata."""
        return [self._mock_model]
