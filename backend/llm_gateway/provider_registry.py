"""Registry of available LLM provider adapter types."""

import threading

from backend.llm_gateway.exceptions import ProviderNotFoundError
from backend.llm_gateway.provider import ILLMProviderAdapter
from backend.llm_gateway.providers import (
    AnthropicLLMProviderAdapter,
    GeminiLLMProviderAdapter,
    MockLLMProviderAdapter,
    OllamaLLMProviderAdapter,
    OpenAILLMProviderAdapter,
)


class ProviderRegistry:
    """Registry maintaining mappings from provider names to adapter classes."""

    def __init__(self) -> None:
        """Initialize registry with standard default providers."""
        self._lock = threading.RLock()
        self._provider_classes: dict[str, type[ILLMProviderAdapter]] = {}

        # Auto-register core supported providers
        self.register_provider_class("mock", MockLLMProviderAdapter)
        self.register_provider_class("openai", OpenAILLMProviderAdapter)
        self.register_provider_class("anthropic", AnthropicLLMProviderAdapter)
        self.register_provider_class("gemini", GeminiLLMProviderAdapter)
        self.register_provider_class("ollama", OllamaLLMProviderAdapter)

    def register_provider_class(
        self, provider_name: str, adapter_class: type[ILLMProviderAdapter]
    ) -> None:
        """Register a provider adapter class by provider name.

        Args:
            provider_name: Canonical provider name string.
            adapter_class: Class implementing ILLMProviderAdapter interface.
        """
        with self._lock:
            self._provider_classes[provider_name.lower()] = adapter_class

    def get_provider_class(
        self, provider_name: str
    ) -> type[ILLMProviderAdapter]:
        """Retrieve provider adapter class by provider name.

        Args:
            provider_name: Target provider name (e.g., 'openai').

        Returns:
            Provider adapter class.

        Raises:
            ProviderNotFoundError: If provider name is unregistered.
        """
        with self._lock:
            name = provider_name.lower()
            if name not in self._provider_classes:
                raise ProviderNotFoundError(
                    f"Unsupported LLM provider '{provider_name}'. "
                    f"Registered providers: {list(self._provider_classes.keys())}"
                )
            return self._provider_classes[name]

    def list_supported_providers(self) -> list[str]:
        """List all registered provider names."""
        with self._lock:
            return list(self._provider_classes.keys())
