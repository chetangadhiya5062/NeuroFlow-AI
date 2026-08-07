"""Agent reasoning context, execution step, and final response models."""

from dataclasses import dataclass, field
from typing import Any

from backend.agent_runtime.action import ActionResult, AgentAction


@dataclass
class AgentStep:
    """Dataclass tracking a single step in the reasoning loop.

    Attributes:
        iteration: Sequential step iteration number (1-indexed).
        action: Chosen AgentAction.
        result: Execution ActionResult payload.
    """

    iteration: int
    action: AgentAction
    result: ActionResult | None = None


@dataclass
class AgentContext:
    """Mutable context state maintaining reasoning trajectory across iterations.

    Attributes:
        goal: User query goal string.
        conversation_id: Associated conversation ID string.
        steps: List of executed AgentSteps.
        sources: Retrieved knowledge sources citations.
        tool_results: Execution results from tools.
        final_answer: Accumulated final text response string.
        completed: Flag indicating if reasoning loop finished.
    """

    goal: str
    conversation_id: str | None = None
    steps: list[AgentStep] = field(default_factory=list)
    sources: list[dict[str, Any]] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    final_answer: str | None = None
    completed: bool = False


@dataclass(frozen=True)
class AgentResponse:
    """Final output response returned by the Agent Runtime.

    Attributes:
        answer: Final text response generated for user goal.
        conversation_id: Conversation ID string.
        iterations: Total reasoning iterations executed.
        sources: Retrieved knowledge sources citations list.
        tool_results: Executed tool results list.
        trajectory: Trace list of reasoning steps.
    """

    answer: str
    conversation_id: str
    iterations: int
    sources: list[dict[str, Any]] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    trajectory: list[dict[str, Any]] = field(default_factory=list)
