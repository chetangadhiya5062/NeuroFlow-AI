"""Ollama local LLM Provider adapter implementation."""

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


class OllamaLLMProviderAdapter(BaseLLMProviderAdapter):
    """Ollama local LLM provider integration adapter using HTTP REST API."""

    def __init__(self, base_url: str | None = None) -> None:
        """Initialize Ollama provider adapter with optional base URL.

        Args:
            base_url: Ollama base server URL string.
        """
        self._base_url = (
            base_url
            or os.getenv("OLLAMA_BASE_URL")
            or "http://localhost:11434"
        ).rstrip("/")
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
        """Execute Ollama /api/chat REST API request.

        Args:
            request: CompletionRequest payload.

        Returns:
            Result wrapping CompletionResponse or ErrorInfo error payload.
        """
        url = f"{self._base_url}/api/chat"

        messages_payload = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        payload: dict[str, Any] = {
            "model": request.model.name,
            "messages": messages_payload,
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=payload)

                if response.status_code != 200:
                    return Err(
                        ErrorInfo(
                            message=(
                                f"Ollama API error ({response.status_code}): "
                                f"{response.text}"
                            ),
                            error_code="OLLAMA_API_ERROR",
                            retryable=True,
                        )
                    )

                data = response.json()
                msg = data.get("message", {})
                content = msg.get("content", "")

                prompt_eval_count = data.get("prompt_eval_count", 0)
                eval_count = data.get("eval_count", 0)
                usage = UsageInfo(
                    prompt_tokens=prompt_eval_count,
                    completion_tokens=eval_count,
                    total_tokens=prompt_eval_count + eval_count,
                    estimated_cost=0.0,
                )

                return Ok(
                    CompletionResponse(
                        id=self._generate_completion_id("ollama"),
                        model=request.model,
                        content=content,
                        usage=usage,
                        finish_reason="stop",
                        raw_response=data,
                    )
                )
        except Exception as exc:
            return Err(
                ErrorInfo(
                    message=f"Ollama connection error at '{self._base_url}': {exc}",
                    error_code="OLLAMA_CONNECTION_ERROR",
                    retryable=True,
                )
            )

    async def generate_stream(
        self, request: CompletionRequest
    ) -> AsyncGenerator[StreamChunk, None]:
        """Yield Ollama streaming response chunk stub."""
        yield StreamChunk(
            id=self._generate_completion_id("ollama-stream"),
            model=request.model,
            delta_content="[Ollama Streaming Placeholder]",
            finish_reason="stop",
        )

    def get_supported_models(self) -> list[ModelMetadata]:
        """Return supported Ollama models."""
        return self._models
