"""Data models, requests, responses, and capability enums for LLM Gateway."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from backend.core.value_objects import ModelIdentifier


class ModelCapability(StrEnum):
    """Capabilities supported by LLM models."""

    TEXT_GENERATION = "TEXT_GENERATION"
    CHAT = "CHAT"
    VISION = "VISION"
    FUNCTION_CALLING = "FUNCTION_CALLING"
    EMBEDDING = "EMBEDDING"
    STREAMING = "STREAMING"
    JSON_OUTPUT = "JSON_OUTPUT"


@dataclass(frozen=True)
class ModelMetadata:
    """Metadata specification for a registered LLM model.

    Attributes:
        model_id: Canonical model identifier.
        provider_name: Target provider name (e.g., 'openai', 'anthropic').
        context_window: Maximum context token limit.
        max_output_tokens: Maximum token generation limit.
        capabilities: Set of capabilities supported by model.
        input_cost_per_1k_tokens: Cost in USD per 1,000 prompt tokens.
        output_cost_per_1k_tokens: Cost in USD per 1,000 completion tokens.
    """

    model_id: ModelIdentifier
    provider_name: str
    context_window: int = 128000
    max_output_tokens: int = 4096
    capabilities: set[ModelCapability] = field(
        default_factory=lambda: {
            ModelCapability.TEXT_GENERATION,
            ModelCapability.CHAT,
            ModelCapability.STREAMING,
        }
    )
    input_cost_per_1k_tokens: float = 0.0015
    output_cost_per_1k_tokens: float = 0.002


@dataclass(frozen=True)
class ChatMessage:
    """Single chat message payload.

    Attributes:
        role: Message role ('system', 'user', 'assistant', 'tool').
        content: Text content of message.
        name: Optional author or function name.
    """

    role: str
    content: str
    name: str | None = None


@dataclass(frozen=True)
class CompletionRequest:
    """Normalized text/chat completion request payload.

    Attributes:
        messages: Sequence of ChatMessage objects.
        model: Target ModelIdentifier.
        temperature: Sampling temperature (0.0 to 2.0).
        max_tokens: Optional maximum tokens to generate.
        top_p: Nucleus sampling parameter.
        stop: Optional list of stop sequence strings.
        stream: Flag indicating if streaming response is requested.
        extra_params: Extensible provider-specific parameters.
    """

    messages: list[ChatMessage]
    model: ModelIdentifier
    temperature: float = 0.7
    max_tokens: int | None = None
    top_p: float = 1.0
    stop: list[str] | None = None
    stream: bool = False
    extra_params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class UsageInfo:
    """Token consumption and cost calculation data.

    Attributes:
        prompt_tokens: Number of prompt tokens used.
        completion_tokens: Number of completion tokens generated.
        total_tokens: Total token sum.
        estimated_cost: Estimated cost in USD.
    """

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float = 0.0


@dataclass(frozen=True)
class CompletionResponse:
    """Normalized completion response payload.

    Attributes:
        id: Response completion identifier.
        model: ModelIdentifier used for generation.
        content: Generated text response content.
        usage: Token consumption and cost info.
        finish_reason: Termination reason ('stop', 'length', 'tool_calls').
        raw_response: Optional raw provider response dictionary.
    """

    id: str
    model: ModelIdentifier
    content: str
    usage: UsageInfo
    finish_reason: str = "stop"
    raw_response: dict[str, Any] | None = None


@dataclass(frozen=True)
class StreamChunk:
    """Incremental streaming response delta chunk.

    Attributes:
        id: Completion stream identifier.
        model: ModelIdentifier generating chunk.
        delta_content: Incremental text delta content.
        finish_reason: Optional finish reason if last chunk.
    """

    id: str
    model: ModelIdentifier
    delta_content: str
    finish_reason: str | None = None
