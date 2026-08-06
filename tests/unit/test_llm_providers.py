"""Unit tests for ProviderFactory, ProviderRegistry, and provider adapters."""

import pytest

from backend.llm_gateway import (
    ProviderFactory,
    ProviderNotFoundError,
    ProviderRegistry,
)
from backend.llm_gateway.providers import (
    AnthropicLLMProviderAdapter,
    GeminiLLMProviderAdapter,
    MockLLMProviderAdapter,
    OllamaLLMProviderAdapter,
    OpenAILLMProviderAdapter,
)


def test_provider_registry_lists_standard_providers() -> None:
    """Test ProviderRegistry registers standard supported providers."""
    registry = ProviderRegistry()
    providers = registry.list_supported_providers()

    assert "mock" in providers
    assert "openai" in providers
    assert "anthropic" in providers
    assert "gemini" in providers
    assert "ollama" in providers


def test_provider_factory_creates_instances() -> None:
    """Test ProviderFactory creates adapter instances for supported providers."""
    factory = ProviderFactory()

    assert isinstance(factory.create_provider("mock"), MockLLMProviderAdapter)
    assert isinstance(
        factory.create_provider("openai"), OpenAILLMProviderAdapter
    )
    assert isinstance(
        factory.create_provider("anthropic"), AnthropicLLMProviderAdapter
    )
    assert isinstance(
        factory.create_provider("gemini"), GeminiLLMProviderAdapter
    )
    assert isinstance(
        factory.create_provider("ollama"), OllamaLLMProviderAdapter
    )


def test_provider_factory_invalid_provider_raises_error() -> None:
    """Test ProviderFactory raises ProviderNotFoundError for unknown provider."""
    factory = ProviderFactory()

    with pytest.raises(ProviderNotFoundError, match="Unsupported LLM provider"):
        factory.create_provider("unsupported-provider")
