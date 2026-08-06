"""Fluent builder for constructing PromptTemplate objects."""

from typing import Self

from backend.prompt_runtime.prompt_template import PromptTemplate, PromptVersion


class PromptBuilder:
    """Builder class constructing PromptTemplate instances."""

    def __init__(self, name: str) -> None:
        """Initialize builder with template name."""
        self._name = name
        self._version = "1.0.0"
        self._system_template: str | None = None
        self._user_template: str = ""
        self._assistant_template: str | None = None
        self._required_variables: set[str] = set()
        self._description: str | None = None

    def with_version(self, version: str) -> Self:
        """Set template version string."""
        self._version = version
        return self

    def with_system(self, system_prompt: str) -> Self:
        """Set system prompt template string."""
        self._system_template = system_prompt
        return self

    def with_user(self, user_prompt: str) -> Self:
        """Set user prompt template string."""
        self._user_template = user_prompt
        return self

    def with_assistant(self, assistant_prompt: str) -> Self:
        """Set assistant prompt template string."""
        self._assistant_template = assistant_prompt
        return self

    def with_variable(self, variable_name: str) -> Self:
        """Explicitly declare a required variable name."""
        self._required_variables.add(variable_name)
        return self

    def with_description(self, description: str) -> Self:
        """Set template description."""
        self._description = description
        return self

    def build(self) -> PromptTemplate:
        """Build and return configured PromptTemplate instance."""
        return PromptTemplate(
            name=self._name,
            version=PromptVersion(version=self._version),
            system_template=self._system_template,
            user_template=self._user_template,
            assistant_template=self._assistant_template,
            required_variables=self._required_variables,
            description=self._description,
        )
