"""Thread-safe registry managing registered tool instances."""

import threading

from backend.tool_runtime.exceptions import ToolNotFoundError
from backend.tool_runtime.metadata import ToolMetadata
from backend.tool_runtime.tool import ITool


class ToolRegistry:
    """Registry maintaining executable tool instances by canonical name."""

    def __init__(self) -> None:
        """Initialize empty tool container and reentrant lock."""
        self._lock = threading.RLock()
        self._tools: dict[str, ITool] = {}

    def register_tool(self, tool: ITool) -> None:
        """Register or update a tool instance in the registry.

        Args:
            tool: ITool instance to register.
        """
        with self._lock:
            name = tool.metadata.name.lower()
            self._tools[name] = tool

    def get_tool(self, name: str) -> ITool:
        """Retrieve registered tool by name.

        Args:
            name: Canonical tool name identifier string.

        Returns:
            Matching ITool instance.

        Raises:
            ToolNotFoundError: If tool is not registered.
        """
        with self._lock:
            key = name.lower()
            if key not in self._tools:
                raise ToolNotFoundError(tool_name=name)
            return self._tools[key]

    def list_tools(self) -> list[ToolMetadata]:
        """List metadata for all registered tools."""
        with self._lock:
            return [t.metadata for t in self._tools.values()]

    def clear(self) -> None:
        """Clear all registered tools."""
        with self._lock:
            self._tools.clear()
