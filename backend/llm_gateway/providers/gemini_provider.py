"""Google Gemini LLM Provider adapter implementation."""

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


class GeminiLLMProviderAdapter(BaseLLMProviderAdapter):
    """Google Gemini LLM provider integration adapter using HTTP REST API."""

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize Gemini provider adapter with optional API key.

        Args:
            api_key: Google Gemini API Key string.
        """
        self._api_key = api_key or os.getenv("GEMINI_API_KEY")
        self._base_url = (
            "https://generativelanguage.googleapis.com/v1beta/models"
        )
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
        """Execute Gemini generateContent REST API request.

        Args:
            request: CompletionRequest payload.

        Returns:
            Result wrapping CompletionResponse or ErrorInfo error payload.
        """
        if not self._api_key:
            return Err(
                ErrorInfo(
                    message=(
                        "Gemini API key missing. Set GEMINI_API_KEY env var."
                    ),
                    error_code="AUTHENTICATION_ERROR",
                )
            )

        model_name = request.model.name
        url = f"{self._base_url}/{model_name}:generateContent?key={self._api_key}"

        contents = []
        for msg in request.messages:
            role = "user" if msg.role == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg.content}]})

        payload: dict[str, Any] = {"contents": contents}

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=payload)

                if response.status_code != 200:
                    return Err(
                        ErrorInfo(
                            message=(
                                f"Gemini API error ({response.status_code}): "
                                f"{response.text}"
                            ),
                            error_code="GEMINI_API_ERROR",
                            retryable=response.status_code in (429, 500, 503),
                        )
                    )

                data = response.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    return Err(
                        ErrorInfo(
                            message="Gemini API returned no response candidates.",
                            error_code="GEMINI_EMPTY_RESPONSE",
                        )
                    )

                parts = candidates[0].get("content", {}).get("parts", [])
                text_content = "".join([p.get("text", "") for p in parts])

                usage_meta = data.get("usageMetadata", {})
                usage = UsageInfo(
                    prompt_tokens=usage_meta.get("promptTokenCount", 0),
                    completion_tokens=usage_meta.get("candidatesTokenCount", 0),
                    total_tokens=usage_meta.get("totalTokenCount", 0),
                )

                return Ok(
                    CompletionResponse(
                        id=self._generate_completion_id("gemini"),
                        model=request.model,
                        content=text_content,
                        usage=usage,
                        finish_reason="stop",
                        raw_response=data,
                    )
                )
        except Exception as exc:
            return Err(
                ErrorInfo(
                    message=f"Gemini connection error: {exc}",
                    error_code="GEMINI_CONNECTION_ERROR",
                    retryable=True,
                )
            )

    async def generate_stream(
        self, request: CompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        """Yield Gemini streaming response chunk stub."""
        yield StreamChunk(
            id=self._generate_completion_id("gemini-stream"),
            model=request.model,
            delta_content="[Gemini Streaming Placeholder]",
            finish_reason="stop",
        )

    def get_supported_models(self) -> list[ModelMetadata]:
        """Return supported Gemini models."""
        return self._models
