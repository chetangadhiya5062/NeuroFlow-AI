"""Agent action types and action execution result models."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class AgentActionType(StrEnum):
    """Enumeration of supported agent reasoning actions."""

    RESPOND = "respond"
    RETRIEVE_KNOWLEDGE = "retrieve_knowledge"
    EXECUTE_TOOL = "execute_tool"


@dataclass(frozen=True)
class AgentAction:
    """Descriptor representing a chosen action by the agent reasoning loop.

    Attributes:
        type: AgentActionType enum value.
        name: Name of target tool or retrieval identifier (if applicable).
        arguments: Keyword arguments payload for action execution.
    """

    type: AgentActionType
    name: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ActionResult:
    """Execution output payload returned by an agent action.

    Attributes:
        action: Executed AgentAction descriptor.
        success: Whether action completed cleanly.
        output: Execution result payload.
        error: Error message string if action failed.
    """

    action: AgentAction
    success: bool
    output: Any
    error: str | None = None
