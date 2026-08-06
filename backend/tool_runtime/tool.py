"""Tool abstract interface contract and execution result model."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from backend.tool_runtime.metadata import ToolMetadata


@dataclass(frozen=True)
class ToolResult:
    """Output payload returned by tool execution.

    Attributes:
        success: Whether execution completed cleanly.
        result: Output payload (dictionary, scalar, string, etc.).
        error: Error message string if failed.
        metadata: Extensible execution metadata.
    """

    success: bool
    result: Any
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ITool(ABC):
    """Abstract interface contract for all executable tools."""

    @property
    @abstractmethod
    def metadata(self) -> ToolMetadata:
        """Return ToolMetadata descriptor."""

    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute tool logic with keyword arguments.

        Args:
            **kwargs: Dynamic arguments matching ToolParameter specifications.

        Returns:
            ToolResult payload.
        """
