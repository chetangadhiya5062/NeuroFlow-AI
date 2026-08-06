"""Master Tool Domain Service for tool execution and intent parsing."""

import re
from typing import Any

from backend.tool_runtime.builtins import (
    CalculatorTool,
    CurrentTimeTool,
    TextLengthTool,
)
from backend.tool_runtime.executor import ToolExecutor
from backend.tool_runtime.metadata import ToolMetadata
from backend.tool_runtime.registry import ToolRegistry
from backend.tool_runtime.tool import ITool, ToolResult


class ToolService:
    """Service managing tool lifecycle, execution, and prompt intent resolution."""

    def __init__(
        self,
        registry: ToolRegistry | None = None,
        executor: ToolExecutor | None = None,
    ) -> None:
        """Initialize ToolService and register default built-in tools."""
        self.registry = registry or ToolRegistry()
        self.executor = executor or ToolExecutor(registry=self.registry)
        self._register_builtins()

    def _register_builtins(self) -> None:
        """Register default platform built-in tools."""
        self.registry.register_tool(CalculatorTool())
        self.registry.register_tool(CurrentTimeTool())
        self.registry.register_tool(TextLengthTool())

    def register_tool(self, tool: ITool) -> None:
        """Register a new tool instance in the registry."""
        self.registry.register_tool(tool)

    async def execute_tool_call(
        self, tool_name: str, arguments: dict[str, Any]
    ) -> ToolResult:
        """Execute registered tool by name with arguments.

        Args:
            tool_name: Canonical tool name string.
            arguments: Dictionary of arguments.

        Returns:
            ToolResult object.
        """
        return await self.executor.execute_tool(tool_name, arguments)

    async def process_prompt_tool_intent(
        self, prompt: str
    ) -> ToolResult | None:
        """Detect and execute tool calls for calculation prompts.

        Args:
            prompt: User prompt string.

        Returns:
            ToolResult if math pattern detected, else None.
        """
        if not prompt or not prompt.strip():
            return None

        # Regex matching arithmetic expressions inside query prompts
        match = re.search(
            r"[\d\s\(\)\+\-\*\/\^\%x×÷,]+[\d\)]", prompt  # noqa: RUF001
        )
        if match:
            candidate = match.group(0).strip()
            # Must contain digits and math operator
            if any(char in candidate for char in "+-*%/×÷x") and any(  # noqa: RUF001
                char.isdigit() for char in candidate
            ):
                return await self.execute_tool_call(
                    "calculator", {"expression": candidate}
                )

        return None

    def list_tools(self) -> list[ToolMetadata]:
        """List metadata for all registered tools."""
        return self.registry.list_tools()
