"""OpenAI LLM Provider adapter implementation."""

import os
from collections.abc import AsyncGenerator
from typing import Any

import httpx

from backend.core.types import Err, ErrorInfo, Ok, Result
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
    """OpenAI LLM provider integration adapter using HTTP REST API."""

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize OpenAI provider adapter with optional API key.

        Args:
            api_key: OpenAI API Key string.
        """
        self._api_key = api_key if api_key is not None else os.getenv("OPENAI_API_KEY")
        self._base_url = "https://api.openai.com/v1"
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
        """Execute OpenAI chat completion REST API request.

        Args:
            request: CompletionRequest payload.

        Returns:
            Result wrapping CompletionResponse or ErrorInfo error payload.
        """
        if not self._api_key:
            return Err(
                ErrorInfo(
                    message=(
                        "OpenAI API key missing. Set OPENAI_API_KEY env var."
                    ),
                    error_code="AUTHENTICATION_ERROR",
                )
            )

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        messages_payload = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        payload: dict[str, Any] = {
            "model": request.model.name,
            "messages": messages_payload,
            "temperature": request.temperature,
            "top_p": request.top_p,
        }
        if request.max_tokens:
            payload["max_tokens"] = request.max_tokens

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self._base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                )

                if response.status_code != 200:
                    return Err(
                        ErrorInfo(
                            message=(
                                f"OpenAI API error ({response.status_code}): "
                                f"{response.text}"
                            ),
                            error_code="OPENAI_API_ERROR",
                            retryable=response.status_code in (429, 500, 502, 503),
                        )
                    )

                data = response.json()
                choice = data["choices"][0]
                content = choice["message"]["content"]
                usage_data = data.get("usage", {})

                usage = UsageInfo(
                    prompt_tokens=usage_data.get("prompt_tokens", 0),
                    completion_tokens=usage_data.get("completion_tokens", 0),
                    total_tokens=usage_data.get("total_tokens", 0),
                )

                return Ok(
                    CompletionResponse(
                        id=data.get("id", self._generate_completion_id("openai")),
                        model=request.model,
                        content=content,
                        usage=usage,
                        finish_reason=choice.get("finish_reason", "stop"),
                        raw_response=data,
                    )
                )
        except Exception as exc:
            return Err(
                ErrorInfo(
                    message=f"OpenAI connection error: {exc}",
                    error_code="OPENAI_CONNECTION_ERROR",
                    retryable=True,
                )
            )

    async def generate_stream(
        self, request: CompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        """Yield OpenAI streaming response chunk stub."""
        yield StreamChunk(
            id=self._generate_completion_id("openai-stream"),
            model=request.model,
            delta_content="[OpenAI Streaming Placeholder]",
            finish_reason="stop",
        )

    def get_supported_models(self) -> list[ModelMetadata]:
        """Return supported OpenAI models."""
        return self._models
