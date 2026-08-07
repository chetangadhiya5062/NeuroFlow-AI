"""Document aggregate root entity definition."""

from dataclasses import dataclass, field

from backend.core.entities import AggregateRoot
from backend.core.value_objects import EntityId, TenantId
from backend.knowledge_base.metadata import DocumentMetadata


@dataclass
class Document(AggregateRoot):
    """Document aggregate root representing an ingested knowledge base entity.

    Attributes:
        id: Unique EntityId for document.
        storage_path: Local file path string where raw file is stored.
        metadata: Associated DocumentMetadata descriptor.
        tenant_id: Optional multi-tenant TenantId.
        project_id: Optional parent Project EntityId.
        workspace_id: Optional parent Workspace EntityId.
    """

    id: EntityId = field(default_factory=EntityId)
    storage_path: str = ""
    metadata: DocumentMetadata = field(
        default_factory=lambda: DocumentMetadata(
            filename="", size_bytes=0, mime_type="", file_extension=""
        )
    )
    tenant_id: TenantId | None = None
    project_id: EntityId | None = None
    workspace_id: EntityId | None = None

    @classmethod
    def create(
        cls,
        storage_path: str,
        metadata: DocumentMetadata,
        tenant_id: TenantId | None = None,
        project_id: EntityId | None = None,
        workspace_id: EntityId | None = None,
    ) -> "Document":
        """Factory method constructing a new Document instance.

        Args:
            storage_path: Saved file path string.
            metadata: DocumentMetadata value object.
            tenant_id: Optional TenantId.
            project_id: Optional Project EntityId.
            workspace_id: Optional Workspace EntityId.

        Returns:
            Instantiated Document aggregate root.
        """
        return cls(
            id=EntityId(),
            storage_path=storage_path,
            metadata=metadata,
            tenant_id=tenant_id,
            project_id=project_id,
            workspace_id=workspace_id,
        )
