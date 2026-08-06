"""Provider router for resolving adapters and executing request dispatching."""

import threading

from backend.llm_gateway.exceptions import (
    ModelCapabilityMismatchError,
    ProviderNotFoundError,
)
from backend.llm_gateway.models import CompletionRequest, ModelCapability
from backend.llm_gateway.provider import ILLMProviderAdapter
from backend.llm_gateway.registry import ModelRegistry


class LLMRouter:
    """Thread-safe router mapping providers and validating completion requests."""

    def __init__(self, registry: ModelRegistry | None = None) -> None:
        """Initialize router with registry and lock."""
        self._lock = threading.RLock()
        self._registry = registry or ModelRegistry()
        self._providers: dict[str, ILLMProviderAdapter] = {}

    def register_provider(self, adapter: ILLMProviderAdapter) -> None:
        """Register provider adapter and auto-register supported models.

        Args:
            adapter: ILLMProviderAdapter instance to register.
        """
        with self._lock:
            name = adapter.provider_name.lower()
            self._providers[name] = adapter
            for model_meta in adapter.get_supported_models():
                self._registry.register_model(model_meta)

    def get_provider(self, provider_name: str) -> ILLMProviderAdapter:
        """Retrieve provider adapter by name.

        Args:
            provider_name: Provider identifier (e.g. 'openai').

        Returns:
            ILLMProviderAdapter instance.

        Raises:
            ProviderNotFoundError: If provider adapter is not registered.
        """
        with self._lock:
            name = provider_name.lower()
            if name not in self._providers:
                raise ProviderNotFoundError(
                    f"No LLM provider adapter registered for '{provider_name}'."
                )
            return self._providers[name]

    def route_request(
        self, request: CompletionRequest
    ) -> ILLMProviderAdapter:
        """Resolve target provider adapter for completion request.

        Args:
            request: CompletionRequest payload.

        Returns:
            Matching ILLMProviderAdapter instance.

        Raises:
            ModelCapabilityMismatchError: If request exceeds model capabilities.
        """
        with self._lock:
            provider_name = request.model.provider.lower()
            adapter = self.get_provider(provider_name)

            # Validate capability requirement if streaming
            if request.stream and self._registry.is_registered(request.model):
                if not self._registry.supports_capability(
                    request.model, ModelCapability.STREAMING
                ):
                    raise ModelCapabilityMismatchError(
                        f"Model '{request.model.canonical_name}' "
                        "does not support STREAMING capability."
                    )

            return adapter
