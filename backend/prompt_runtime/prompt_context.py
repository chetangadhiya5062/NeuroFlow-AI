"""Execution context for prompt compilation and rendering."""

from dataclasses import dataclass, field
from typing import Any

from backend.llm_gateway.models import ChatMessage
from backend.prompt_runtime.prompt_variables import PromptVariables


@dataclass
class PromptContext:
    """Context state passed to prompt renderers and compilers.

    Attributes:
        variables: PromptVariables container holding template variables.
        conversation_history: List of past ChatMessage objects.
        system_override: Optional system prompt text override.
        metadata: Extensible metadata dictionary.
    """

    variables: PromptVariables = field(default_factory=PromptVariables)
    conversation_history: list[ChatMessage] = field(default_factory=list)
    system_override: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
