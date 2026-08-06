"""Variable container and text template substitution manager."""

import re
from dataclasses import dataclass, field
from typing import Any

from backend.prompt_runtime.exceptions import PromptRenderError


@dataclass(frozen=True)
class PromptVariables:
    """Immutable variable mapping for prompt template interpolation.

    Attributes:
        variables: Key-value mapping of template variables.
    """

    variables: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        """Get variable value by key name."""
        return self.variables.get(key, default)

    def contains(self, key: str) -> bool:
        """Check if key exists in variables."""
        return key in self.variables

    def substitute_in_text(self, template_text: str) -> str:
        """Perform {variable_name} placeholder substitution in template text.

        Args:
            template_text: Template string containing {var} placeholders.

        Returns:
            Substituted string value.

        Raises:
            PromptRenderError: If required variable placeholder is missing.
        """
        if not template_text:
            return ""

        pattern = re.compile(r"\{([a-zA-Z0-9_]+)\}")

        def replace_match(match: re.Match[str]) -> str:
            var_name = match.group(1)
            if var_name in self.variables:
                return str(self.variables[var_name])
            raise PromptRenderError(
                f"Missing required variable '{var_name}' for prompt template."
            )

        try:
            return pattern.sub(replace_match, template_text)
        except PromptRenderError:
            raise
        except Exception as exc:
            raise PromptRenderError(
                f"Failed to substitute variables in template: {exc}"
            ) from exc
