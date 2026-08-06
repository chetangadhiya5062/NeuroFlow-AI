"""Pipeline response payload definition."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PipelineResponse:
    """Output response payload produced by the AI Request Pipeline.

    Attributes:
        content: Generated text response content string.
        conversation_id: Associated conversation EntityId string.
        model_used: ModelIdentifier canonical name used for generation.
        provider_used: Target provider name used for generation.
        tokens_used: Total token count consumed.
        estimated_cost: Estimated generation cost in USD.
        metadata: Extensible response metadata dictionary.
    """

    content: str
    conversation_id: str
    model_used: str
    provider_used: str
    tokens_used: int = 0
    estimated_cost: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
