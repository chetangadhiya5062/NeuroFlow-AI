"""Pipeline request payload definition."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PipelineRequest:
    """Input request payload passed into the AI Request Pipeline.

    Attributes:
        prompt: Primary user prompt string.
        conversation_id: Optional existing conversation EntityId or string.
        model_name: Optional explicit model override string.
        provider_name: Optional explicit provider override string.
        metadata: Extensible request metadata dictionary.
    """

    prompt: str
    conversation_id: str | None = None
    model_name: str | None = None
    provider_name: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
