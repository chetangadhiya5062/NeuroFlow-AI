"""Pipeline execution context mutable container."""

from dataclasses import dataclass, field
from typing import Any

from backend.conversation import Conversation
from backend.core.value_objects import ModelIdentifier
from backend.llm_gateway import CompletionRequest, CompletionResponse
from backend.pipeline.request import PipelineRequest
from backend.pipeline.response import PipelineResponse


@dataclass
class PipelineContext:
    """Mutable context state passed through pipeline processors and middlewares.

    Attributes:
        request: Incoming PipelineRequest input.
        conversation: Associated Conversation aggregate root.
        model_id: Target ModelIdentifier resolved for generation.
        formatted_prompt: Processed prompt string (Prompt Runtime placeholder).
        llm_request: Prepared LLM CompletionRequest payload.
        llm_response: Returned LLM CompletionResponse payload.
        final_response: Constructed PipelineResponse output.
        metadata: Extensible execution metadata dictionary.
    """

    request: PipelineRequest
    conversation: Conversation | None = None
    model_id: ModelIdentifier | None = None
    formatted_prompt: str | None = None
    llm_request: CompletionRequest | None = None
    llm_response: CompletionResponse | None = None
    final_response: PipelineResponse | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
