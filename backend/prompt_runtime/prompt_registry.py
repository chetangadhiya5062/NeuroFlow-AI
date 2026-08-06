"""Thread-safe registry managing registered prompt templates."""

import threading

from backend.prompt_runtime.exceptions import PromptNotFoundError
from backend.prompt_runtime.prompt_template import PromptTemplate


class PromptRegistry:
    """Registry maintaining prompt templates by name and version."""

    def __init__(self) -> None:
        """Initialize registry container and reentrant lock."""
        self._lock = threading.RLock()
        self._templates: dict[str, dict[str, PromptTemplate]] = {}

    def register_template(self, template: PromptTemplate) -> None:
        """Register or update a prompt template in the registry.

        Args:
            template: PromptTemplate to register.
        """
        with self._lock:
            name = template.name.lower()
            if name not in self._templates:
                self._templates[name] = {}
            self._templates[name][template.version.version] = template

    def get_template(
        self, name: str, version: str | None = None
    ) -> PromptTemplate:
        """Retrieve registered prompt template by name and optional version.

        Args:
            name: Template name identifier string.
            version: Optional version string (defaults to latest or '1.0.0').

        Returns:
            Matching PromptTemplate.

        Raises:
            PromptNotFoundError: If template or version is not found.
        """
        with self._lock:
            key = name.lower()
            if key not in self._templates:
                raise PromptNotFoundError(template_name=name, version=version)

            versions_dict = self._templates[key]
            if version:
                if version not in versions_dict:
                    raise PromptNotFoundError(template_name=name, version=version)
                return versions_dict[version]

            # Return latest version registered
            latest_version = max(versions_dict.keys())
            return versions_dict[latest_version]

    def list_templates(self) -> list[PromptTemplate]:
        """List all registered prompt templates across all versions."""
        with self._lock:
            result: list[PromptTemplate] = []
            for ver_map in self._templates.values():
                result.extend(ver_map.values())
            return result

    def clear(self) -> None:
        """Clear all registered prompt templates."""
        with self._lock:
            self._templates.clear()
