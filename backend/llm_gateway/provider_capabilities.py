"""Provider and model capability declarations for LLM Gateway."""

from backend.llm_gateway.models import ModelCapability

# ProviderCapability is an alias to ModelCapability for unified capability tracking
ProviderCapability = ModelCapability

__all__ = ["ModelCapability", "ProviderCapability"]
