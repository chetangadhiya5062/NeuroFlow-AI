"""Platform configuration and dependency injection container for NeuroFlow AI."""

from backend.config.container import (
    DependencyResolver,
    ServiceContainer,
    ServiceLifetime,
    ServiceRegistration,
    ServiceRegistry,
    get_container,
)
from backend.config.provider import PydanticConfigurationProvider
from backend.config.settings import (
    AppSettings,
    DatabaseSettings,
    FeatureFlagSettings,
    LLMSettings,
    LoggingSettings,
    RuntimeSettings,
    Settings,
    get_settings,
)

__all__ = [
    "AppSettings",
    "DatabaseSettings",
    "DependencyResolver",
    "FeatureFlagSettings",
    "LLMSettings",
    "LoggingSettings",
    "PydanticConfigurationProvider",
    "RuntimeSettings",
    "ServiceContainer",
    "ServiceLifetime",
    "ServiceRegistration",
    "ServiceRegistry",
    "Settings",
    "get_container",
    "get_settings",
]
