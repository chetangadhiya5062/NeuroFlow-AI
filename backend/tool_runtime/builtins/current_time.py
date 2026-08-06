"""Current Time built-in tool implementation."""

from datetime import UTC, datetime
from typing import Any

from backend.tool_runtime.metadata import ToolMetadata
from backend.tool_runtime.tool import ITool, ToolResult


class CurrentTimeTool(ITool):
    """Built-in tool returning current UTC timestamp and datetime details."""

    @property
    def metadata(self) -> ToolMetadata:
        """Return CurrentTime tool metadata."""
        return ToolMetadata(
            name="current_time",
            description="Returns current UTC timestamp and ISO datetime information.",
            parameters=[],
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute current time fetch.

        Returns:
            ToolResult containing ISO datetime string and timestamp info.
        """
        now = datetime.now(UTC)
        time_info = {
            "iso": now.isoformat(),
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "second": now.second,
            "timezone": "UTC",
        }
        return ToolResult(
            success=True,
            result=time_info,
            metadata={"timestamp_utc": now.isoformat()},
        )
