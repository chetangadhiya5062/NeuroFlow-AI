"""Workspace aggregate root domain entity definition."""

from dataclasses import dataclass, field

from backend.core.entities import AggregateRoot
from backend.core.value_objects import EntityId, TenantId, Timestamp


@dataclass
class Workspace(AggregateRoot):
    """Workspace aggregate root representing a multi-tenant workspace boundary.

    Attributes:
        id: Unique EntityId for workspace.
        name: Workspace display name.
        owner_id: EntityId of owning User.
        tenant_id: Associated multi-tenant TenantId.
        created_at: Creation Timestamp.
    """

    name: str = ""
    owner_id: EntityId = field(default_factory=EntityId)
    id: EntityId = field(default_factory=EntityId)
    tenant_id: TenantId = field(
        default_factory=lambda: TenantId(str(EntityId().value))
    )
    created_at: Timestamp = field(default_factory=Timestamp)

    @classmethod
    def create(cls, name: str, owner_id: EntityId) -> "Workspace":
        """Factory method constructing a new Workspace aggregate.

        Args:
            name: Workspace name string.
            owner_id: EntityId of owner user.

        Returns:
            Instantiated Workspace aggregate root.
        """
        wid = EntityId()
        return cls(
            id=wid,
            name=name,
            owner_id=owner_id,
            tenant_id=TenantId(wid.value),
            created_at=Timestamp(),
        )
