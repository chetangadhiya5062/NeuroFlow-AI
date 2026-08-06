"""Unit tests for production LLM Provider Adapters."""

import pytest

from backend.core.value_objects import ModelIdentifier
from backend.llm_gateway.models import ChatMessage, CompletionRequest
from backend.llm_gateway.providers import (
    AnthropicLLMProviderAdapter,
    GeminiLLMProviderAdapter,
    MockLLMProviderAdapter,
    OllamaLLMProviderAdapter,
    OpenAILLMProviderAdapter,
)


@pytest.mark.asyncio
async def test_openai_provider_missing_key_returns_auth_error() -> None:
    """Test OpenAI provider returns AUTHENTICATION_ERROR when API key is empty."""
    adapter = OpenAILLMProviderAdapter(api_key="")
    req = CompletionRequest(
        messages=[ChatMessage(role="user", content="Hi")],
        model=ModelIdentifier(name="gpt-4o", provider="openai"),
    )
    res = await adapter.generate_completion(req)
    assert not res.is_success
    err = res.unwrap_err()
    assert err.error_code == "AUTHENTICATION_ERROR"
    assert "OPENAI_API_KEY" in err.message


@pytest.mark.asyncio
async def test_gemini_provider_missing_key_returns_auth_error() -> None:
    """Test Gemini provider returns AUTHENTICATION_ERROR when API key is empty."""
    adapter = GeminiLLMProviderAdapter(api_key="")
    req = CompletionRequest(
        messages=[ChatMessage(role="user", content="Hi")],
        model=ModelIdentifier(name="gemini-1.5-pro", provider="gemini"),
    )
    res = await adapter.generate_completion(req)
    assert not res.is_success
    err = res.unwrap_err()
    assert err.error_code == "AUTHENTICATION_ERROR"
    assert "GEMINI_API_KEY" in err.message


@pytest.mark.asyncio
async def test_ollama_provider_connection_error_handling() -> None:
    """Test Ollama provider returns OLLAMA_CONNECTION_ERROR when server unreachable."""
    adapter = OllamaLLMProviderAdapter(base_url="http://invalid-localhost:99999")
    req = CompletionRequest(
        messages=[ChatMessage(role="user", content="Hi")],
        model=ModelIdentifier(name="llama3", provider="ollama"),
    )
    res = await adapter.generate_completion(req)
    assert not res.is_success
    err = res.unwrap_err()
    assert err.error_code == "OLLAMA_CONNECTION_ERROR"


@pytest.mark.asyncio
async def test_anthropic_placeholder_provider() -> None:
    """Test Anthropic provider placeholder response."""
    adapter = AnthropicLLMProviderAdapter()
    req = CompletionRequest(
        messages=[ChatMessage(role="user", content="Hi")],
        model=ModelIdentifier(name="claude-3-5-sonnet-latest", provider="anthropic"),
    )
    res = await adapter.generate_completion(req)
    assert res.is_success
    assert "Anthropic Provider Adapter" in res.unwrap().content


@pytest.mark.asyncio
async def test_mock_provider() -> None:
    """Test Mock LLM provider adapter response."""
    adapter = MockLLMProviderAdapter()
    req = CompletionRequest(
        messages=[ChatMessage(role="user", content="Hi")],
        model=ModelIdentifier(name="mock-model", provider="mock"),
    )
    res = await adapter.generate_completion(req)
    assert res.is_success
    assert "Mock Provider" in res.unwrap().content
