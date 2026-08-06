"""Tool executor validating parameter schemas and executing tools."""

from typing import Any

from backend.tool_runtime.exceptions import (
    ToolExecutionError,
    ToolValidationError,
)
from backend.tool_runtime.registry import ToolRegistry
from backend.tool_runtime.tool import ToolResult


class ToolExecutor:
    """Executor validating arguments and executing target tool logic."""

    def __init__(self, registry: ToolRegistry) -> None:
        """Initialize ToolExecutor with ToolRegistry dependency."""
        self._registry = registry

    async def execute_tool(
        self, tool_name: str, arguments: dict[str, Any]
    ) -> ToolResult:
        """Validate parameter requirements and execute tool asynchronously.

        Args:
            tool_name: Canonical tool name string.
            arguments: Dictionary of arguments matching tool parameters.

        Returns:
            ToolResult containing execution outcome payload.

        Raises:
            ToolNotFoundError: If tool is missing from registry.
            ToolValidationError: If required arguments are missing.
        """
        tool = self._registry.get_tool(tool_name)
        meta = tool.metadata

        # Validate required parameters
        missing_params = [
            p.name
            for p in meta.parameters
            if p.required and p.name not in arguments
        ]

        if missing_params:
            raise ToolValidationError(
                f"Missing required parameters for tool '{tool_name}': "
                f"{', '.join(missing_params)}"
            )

        try:
            return await tool.execute(**arguments)
        except ToolValidationError:
            raise
        except Exception as exc:
            raise ToolExecutionError(
                tool_name=tool_name, reason=str(exc)
            ) from exc
