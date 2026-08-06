"""Thread-safe model registry for managing model metadata and capabilities."""

import threading

from backend.core.value_objects import ModelIdentifier
from backend.llm_gateway.exceptions import ModelNotFoundError
from backend.llm_gateway.models import ModelCapability, ModelMetadata


class ModelRegistry:
    """Thread-safe registry managing model metadata and capability mappings."""

    def __init__(self) -> None:
        """Initialize registry container and synchronization lock."""
        self._lock = threading.RLock()
        self._models: dict[str, ModelMetadata] = {}

    def register_model(self, metadata: ModelMetadata) -> None:
        """Register or update model metadata in registry.

        Args:
            metadata: ModelMetadata specification to register.
        """
        with self._lock:
            key = metadata.model_id.canonical_name
            self._models[key] = metadata

    def get_model(self, model_id: ModelIdentifier) -> ModelMetadata:
        """Retrieve model metadata by ModelIdentifier.

        Args:
            model_id: Target ModelIdentifier.

        Returns:
            ModelMetadata instance.

        Raises:
            ModelNotFoundError: If model is not registered.
        """
        with self._lock:
            key = model_id.canonical_name
            if key not in self._models:
                raise ModelNotFoundError(
                    f"Model '{key}' is not registered in ModelRegistry."
                )
            return self._models[key]

    def is_registered(self, model_id: ModelIdentifier) -> bool:
        """Check if a model identifier is registered."""
        with self._lock:
            return model_id.canonical_name in self._models

    def list_models(
        self, capability: ModelCapability | None = None
    ) -> list[ModelMetadata]:
        """List registered models, optionally filtering by capability.

        Args:
            capability: Optional ModelCapability filter.

        Returns:
            List of matching ModelMetadata instances.
        """
        with self._lock:
            if capability is None:
                return list(self._models.values())
            return [
                meta
                for meta in self._models.values()
                if capability in meta.capabilities
            ]

    def supports_capability(
        self, model_id: ModelIdentifier, capability: ModelCapability
    ) -> bool:
        """Check if model supports a specific capability.

        Args:
            model_id: Target ModelIdentifier.
            capability: Capability to check.

        Returns:
            True if model is registered and supports capability, False otherwise.
        """
        with self._lock:
            key = model_id.canonical_name
            if key not in self._models:
                return False
            return capability in self._models[key].capabilities

    def clear(self) -> None:
        """Clear all registered models."""
        with self._lock:
            self._models.clear()
