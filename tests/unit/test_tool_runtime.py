"""Unit and integration tests for Tool Runtime subsystem."""

import pytest
from fastapi.testclient import TestClient

from backend.api.app import get_application
from backend.tool_runtime import (
    CalculatorTool,
    CurrentTimeTool,
    TextLengthTool,
    ToolExecutor,
    ToolRegistry,
    ToolValidationError,
)


@pytest.mark.asyncio
async def test_calculator_built_in_tool() -> None:
    """Test CalculatorTool evaluates arithmetic expressions cleanly."""
    calc = CalculatorTool()

    # Test multiplication and addition: (5432 * 92) + 871
    res1 = await calc.execute(expression="(5432 * 92) + 871")
    assert res1.success
    assert res1.result == 500615

    # Test Unicode multiplication symbol: (5432 × 92) + 871  # noqa: RUF003
    res2 = await calc.execute(expression="(5432 × 92) + 871")  # noqa: RUF001
    assert res2.success
    assert res2.result == 500615


@pytest.mark.asyncio
async def test_current_time_built_in_tool() -> None:
    """Test CurrentTimeTool returns valid UTC timestamp."""
    time_tool = CurrentTimeTool()
    res = await time_tool.execute()
    assert res.success
    assert "iso" in res.result
    assert res.result["timezone"] == "UTC"


@pytest.mark.asyncio
async def test_text_length_built_in_tool() -> None:
    """Test TextLengthTool computes character and word metrics."""
    length_tool = TextLengthTool()
    res = await length_tool.execute(text="NeuroFlow AI Platform")
    assert res.success
    assert res.result["character_count"] == 21
    assert res.result["word_count"] == 3


@pytest.mark.asyncio
async def test_tool_executor_validation() -> None:
    """Test ToolExecutor raises ToolValidationError for missing parameters."""
    registry = ToolRegistry()
    registry.register_tool(CalculatorTool())
    executor = ToolExecutor(registry=registry)

    with pytest.raises(ToolValidationError):
        await executor.execute_tool("calculator", arguments={})


def test_end_to_end_math_chat_flow() -> None:
    """Test end-to-end chat completion executing tool."""
    app = get_application()
    client = TestClient(app)

    response = client.post(
        "/chat",
        json={"message": "What is (5432 × 92) + 871?"},  # noqa: RUF001
    )
    assert response.status_code == 200
    data = response.json()
    assert "500,615" in data["response"] or "500615" in data["response"]
