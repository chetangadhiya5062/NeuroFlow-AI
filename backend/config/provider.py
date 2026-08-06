"""Configuration provider implementing Layer 0 IConfigurationProvider port."""

from typing import Any

from pydantic import BaseModel

from backend.config.settings import Settings, get_settings
from backend.core.ports import IConfigurationProvider


class PydanticConfigurationProvider(IConfigurationProvider):
    """Pydantic-backed configuration provider implementing IConfigurationProvider."""

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize provider with explicit or default singleton settings."""
        self._settings = settings or get_settings()

    def get[T](self, key: str, default: T | None = None) -> T | None:
        """Retrieve nested configuration value by dot-notation key.

        Args:
            key: Dot-separated key (e.g. 'app.environment', 'database.host').
            default: Default value if key is not found.

        Returns:
            Resolved configuration value or default fallback.
        """
        parts = key.split(".")
        current: Any = self._settings
        for part in parts:
            if isinstance(current, BaseModel) and hasattr(current, part):
                current = getattr(current, part)
            elif isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current  # type: ignore[no-any-return]

    def has(self, key: str) -> bool:
        """Check if a dot-notation configuration key exists."""
        sentinel = object()
        return self.get(key, default=sentinel) is not sentinel
