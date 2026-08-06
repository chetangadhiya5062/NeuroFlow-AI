"""Text Length built-in tool implementation."""

from typing import Any

from backend.tool_runtime.metadata import ToolMetadata, ToolParameter
from backend.tool_runtime.tool import ITool, ToolResult


class TextLengthTool(ITool):
    """Built-in tool calculating character, word, and line metrics of text."""

    @property
    def metadata(self) -> ToolMetadata:
        """Return TextLength tool metadata."""
        return ToolMetadata(
            name="text_length",
            description="Calculates character, word, and line count of text.",
            parameters=[
                ToolParameter(
                    name="text",
                    type="str",
                    description="Input text content to analyze.",
                    required=True,
                )
            ],
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute text metrics calculation.

        Args:
            text: Input string payload.

        Returns:
            ToolResult containing character_count, word_count, and line_count.
        """
        text = kwargs.get("text", "")
        text_str = str(text)

        char_count = len(text_str)
        word_count = len(text_str.split()) if text_str.strip() else 0
        line_count = len(text_str.splitlines()) if text_str else 0

        metrics = {
            "character_count": char_count,
            "word_count": word_count,
            "line_count": line_count,
        }

        return ToolResult(
            success=True,
            result=metrics,
            metadata=metrics,
        )
