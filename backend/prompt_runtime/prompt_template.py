"""Prompt template and versioning specifications."""

import re
from dataclasses import dataclass, field

from backend.core.value_objects import EntityId, Timestamp


@dataclass(frozen=True)
class PromptVersion:
    """Version specification for prompt templates.

    Attributes:
        version: Version string (e.g. '1.0.0').
        created_at: Creation Timestamp.
    """

    version: str = "1.0.0"
    created_at: Timestamp = field(default_factory=Timestamp)


@dataclass(frozen=True)
class PromptTemplate:
    """Immutable specification for a registered prompt template.

    Attributes:
        id: Unique EntityId for template.
        name: Canonical prompt template name identifier.
        version: PromptVersion specification.
        system_template: Optional system prompt template string.
        user_template: Required user prompt template string.
        assistant_template: Optional assistant pre-fill template string.
        required_variables: Set of variable names required in template.
        description: Optional template description string.
    """

    name: str
    user_template: str
    id: EntityId = field(default_factory=EntityId)
    version: PromptVersion = field(default_factory=PromptVersion)
    system_template: str | None = None
    assistant_template: str | None = None
    required_variables: set[str] = field(default_factory=set)
    description: str | None = None

    def __post_init__(self) -> None:
        """Extract required variables automatically if required_variables is empty."""
        if not self.required_variables:
            vars_found = set()
            pattern = re.compile(r"\{([a-zA-Z0-9_]+)\}")
            for tmpl in (
                self.system_template,
                self.user_template,
                self.assistant_template,
            ):
                if tmpl:
                    vars_found.update(pattern.findall(tmpl))
            object.__setattr__(self, "required_variables", vars_found)
