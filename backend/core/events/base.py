"""Base domain event models and classification types for NeuroFlow AI."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from backend.core.value_objects import (
    CorrelationId,
    EntityId,
    TenantId,
    Timestamp,
    Version,
)


class EventCategory(StrEnum):
    """Categorization enumeration for domain events."""

    SYSTEM = "SYSTEM"
    WORKFLOW = "WORKFLOW"
    AGENT = "AGENT"
    TOOL = "TOOL"
    KNOWLEDGE = "KNOWLEDGE"
    MEMORY = "MEMORY"
    INTEGRATION = "INTEGRATION"


class EventPriority(StrEnum):
    """Priority level enumeration for domain events."""

    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class EventMetadata:
    """Immutable header container for event correlation and tracing metadata.

    Attributes:
        event_id: Unique event identifier.
        timestamp: Timezone-aware UTC event timestamp.
        tenant_id: Optional tenant identifier for multi-tenant isolation.
        correlation_id: Optional correlation identifier for request tracing.
        causation_id: Optional event ID of the causal predecessor event.
        version: Schema version of the event format.
        priority: Priority classification for event dispatching.
        attributes: Additional extensible key-value metadata attributes.
    """

    event_id: EntityId = field(default_factory=EntityId)
    timestamp: Timestamp = field(default_factory=Timestamp)
    tenant_id: TenantId | None = None
    correlation_id: CorrelationId | None = None
    causation_id: EntityId | None = None
    version: Version = field(default_factory=lambda: Version(1))
    priority: EventPriority = EventPriority.NORMAL
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize EventMetadata to dictionary representation."""
        return {
            "event_id": str(self.event_id),
            "timestamp": str(self.timestamp),
            "tenant_id": str(self.tenant_id) if self.tenant_id else None,
            "correlation_id": (
                str(self.correlation_id) if self.correlation_id else None
            ),
            "causation_id": str(self.causation_id) if self.causation_id else None,
            "version": str(self.version),
            "priority": self.priority.value,
            "attributes": self.attributes,
        }


@dataclass(frozen=True)
class DomainEvent:
    """Base immutable abstract class for all domain events in NeuroFlow AI.

    Attributes:
        metadata: Header metadata containing identity, trace, and tenant context.
        category: Event classification domain category.
    """

    metadata: EventMetadata = field(default_factory=EventMetadata)
    category: EventCategory = EventCategory.SYSTEM

    @property
    def event_name(self) -> str:
        """Return the canonical name of the domain event."""
        return self.__class__.__name__

    def to_dict(self) -> dict[str, Any]:
        """Serialize domain event to dictionary payload representation."""
        return {
            "event_name": self.event_name,
            "category": self.category.value,
            "metadata": self.metadata.to_dict(),
        }
