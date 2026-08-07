"""Project aggregate root domain entity definition."""

from dataclasses import dataclass, field

from backend.core.entities import AggregateRoot
from backend.core.value_objects import EntityId, Timestamp


@dataclass
class Project(AggregateRoot):
    """Project aggregate root representing a project container within a Workspace.

    Attributes:
        id: Unique EntityId for project.
        workspace_id: Parent Workspace EntityId.
        name: Project name string.
        description: Optional project description string.
        created_at: Creation Timestamp.
    """

    workspace_id: EntityId = field(default_factory=EntityId)
    name: str = ""
    description: str | None = None
    id: EntityId = field(default_factory=EntityId)
    created_at: Timestamp = field(default_factory=Timestamp)

    @classmethod
    def create(
        cls,
        workspace_id: EntityId,
        name: str,
        description: str | None = None,
    ) -> "Project":
        """Factory method constructing a new Project aggregate.

        Args:
            workspace_id: Parent Workspace EntityId.
            name: Project display name string.
            description: Optional project description string.

        Returns:
            Instantiated Project aggregate root.
        """
        return cls(
            id=EntityId(),
            workspace_id=workspace_id,
            name=name,
            description=description,
            created_at=Timestamp(),
        )
