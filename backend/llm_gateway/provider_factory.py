"""Factory for instantiating LLM provider adapters dynamically."""

from backend.config import Settings
from backend.llm_gateway.provider import ILLMProviderAdapter
from backend.llm_gateway.provider_registry import ProviderRegistry


class ProviderFactory:
    """Factory creating ILLMProviderAdapter instances based on configuration."""

    def __init__(
        self,
        registry: ProviderRegistry | None = None,
        settings: Settings | None = None,
    ) -> None:
        """Initialize ProviderFactory with registry and platform settings.

        Args:
            registry: Optional explicit ProviderRegistry instance.
            settings: Optional explicit Settings instance.
        """
        self._registry = registry or ProviderRegistry()
        self._settings = settings

    def create_provider(
        self,
        provider_name: str,
        settings: Settings | None = None,
    ) -> ILLMProviderAdapter:
        """Instantiate and return adapter instance for provider_name using settings.

        Args:
            provider_name: Target provider name (e.g. 'mock', 'openai', 'gemini').
            settings: Optional explicit Settings instance.

        Returns:
            Instantiated ILLMProviderAdapter object.
        """
        active_settings = settings or self._settings
        adapter_class = self._registry.get_provider_class(provider_name)
        p_name = provider_name.lower()

        if p_name == "openai":
            api_key = active_settings.llm.openai_api_key if active_settings else None
            return adapter_class(api_key=api_key)  # type: ignore[call-arg]
        if p_name == "gemini":
            api_key = active_settings.llm.gemini_api_key if active_settings else None
            return adapter_class(api_key=api_key)  # type: ignore[call-arg]
        if p_name == "ollama":
            base_url = (
                active_settings.llm.ollama_base_url
                if active_settings
                else "http://localhost:11434"
            )
            return adapter_class(base_url=base_url)  # type: ignore[call-arg]
        if p_name == "anthropic":
            api_key = active_settings.llm.anthropic_api_key if active_settings else None
            return adapter_class(api_key=api_key)  # type: ignore[call-arg]

        return adapter_class()
