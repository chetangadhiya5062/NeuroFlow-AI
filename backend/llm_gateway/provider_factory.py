"""Factory for instantiating LLM provider adapters dynamically."""

from backend.llm_gateway.provider import ILLMProviderAdapter
from backend.llm_gateway.provider_registry import ProviderRegistry


class ProviderFactory:
    """Factory creating ILLMProviderAdapter instances."""

    def __init__(self, registry: ProviderRegistry | None = None) -> None:
        """Initialize ProviderFactory with ProviderRegistry.

        Args:
            registry: Optional explicit ProviderRegistry instance.
        """
        self._registry = registry or ProviderRegistry()

    def create_provider(self, provider_name: str) -> ILLMProviderAdapter:
        """Instantiate and return adapter instance for provider_name.

        Args:
            provider_name: Target provider name (e.g. 'mock', 'openai', 'anthropic').

        Returns:
            Instantiated ILLMProviderAdapter object.
        """
        adapter_class = self._registry.get_provider_class(provider_name)
        return adapter_class()
