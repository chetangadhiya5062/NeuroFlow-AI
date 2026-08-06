"""Unit tests for Prompt Runtime subsystem."""

import pytest

from backend.prompt_runtime import (
    PromptBuilder,
    PromptCompiler,
    PromptContext,
    PromptRegistry,
    PromptRenderer,
    PromptRenderError,
    PromptService,
    PromptValidationError,
    PromptVariables,
)


def test_prompt_variables_substitution() -> None:
    """Test PromptVariables text placeholder substitution."""
    vars_container = PromptVariables(variables={"name": "Alice", "role": "Engineer"})
    result = vars_container.substitute_in_text("Hello {name}, role: {role}")
    assert result == "Hello Alice, role: Engineer"


def test_prompt_variables_missing_var_raises_error() -> None:
    """Test PromptVariables raises PromptRenderError when variable is missing."""
    vars_container = PromptVariables(variables={"name": "Alice"})
    with pytest.raises(PromptRenderError, match="Missing required variable"):
        vars_container.substitute_in_text("Hello {name}, role: {role}")


def test_prompt_builder_and_registry() -> None:
    """Test PromptBuilder constructs PromptTemplate and registers in PromptRegistry."""
    template = (
        PromptBuilder("greeting")
        .with_version("1.0.0")
        .with_system("You are a helpful assistant.")
        .with_user("Hello {user_name}")
        .build()
    )

    registry = PromptRegistry()
    registry.register_template(template)

    fetched = registry.get_template("greeting")
    assert fetched.name == "greeting"
    assert fetched.user_template == "Hello {user_name}"
    assert "user_name" in fetched.required_variables


def test_prompt_compiler_and_renderer() -> None:
    """Test PromptCompiler validation and PromptRenderer ChatMessage generation."""
    template = (
        PromptBuilder("chat-template")
        .with_system("System instructions for {app_name}")
        .with_user("Query: {query}")
        .build()
    )

    compiler = PromptCompiler()
    renderer = PromptRenderer()

    # Valid context
    ctx = PromptContext(
        variables=PromptVariables(
            variables={"app_name": "NeuroFlow", "query": "Status check"}
        )
    )
    compiled = compiler.compile(template, ctx)
    messages = renderer.render(compiled)

    assert len(messages) == 2
    assert messages[0].role == "system"
    assert messages[0].content == "System instructions for NeuroFlow"
    assert messages[1].role == "user"
    assert messages[1].content == "Query: Status check"


def test_prompt_compiler_missing_variable_raises_validation_error() -> None:
    """Test PromptCompiler raises PromptValidationError when variable is missing."""
    template = (
        PromptBuilder("strict-template")
        .with_user("User: {username}")
        .build()
    )

    compiler = PromptCompiler()
    ctx = PromptContext(variables=PromptVariables(variables={}))

    with pytest.raises(PromptValidationError, match="Missing required variables"):
        compiler.compile(template, ctx)


@pytest.mark.asyncio
async def test_prompt_service_format_user_prompt() -> None:
    """Test PromptService format_user_prompt formatting."""
    service = PromptService()
    formatted = await service.format_user_prompt("Hello {user}", {"user": "Bob"})
    assert formatted == "Hello Bob"
