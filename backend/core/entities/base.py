"""Base domain entity and aggregate root models for NeuroFlow AI."""

from dataclasses import dataclass, field
from typing import Any

from backend.core.events import DomainEvent
from backend.core.value_objects import EntityId, Timestamp, Version


@dataclass(eq=False)
class Entity:
    """Base class for domain entities with identity and lifecycle timestamps.

    Equality and hashing are determined strictly by entity identity (`id`).

    Attributes:
        id: Unique entity identifier.
        created_at: Timezone-aware creation timestamp.
        updated_at: Timezone-aware last updated timestamp.
        version: Monotonic version number for optimistic concurrency.
    """

    id: EntityId = field(default_factory=EntityId)
    created_at: Timestamp = field(default_factory=Timestamp)
    updated_at: Timestamp = field(default_factory=Timestamp)
    version: Version = field(default_factory=lambda: Version(1))

    def touch(self) -> None:
        """Update the updated_at timestamp to current UTC time."""
        object.__setattr__(self, "updated_at", Timestamp())

    def increment_version(self) -> None:
        """Increment the entity version number and update touch timestamp."""
        object.__setattr__(self, "version", self.version.next_version())
        self.touch()

    def __eq__(self, other: Any) -> bool:
        """Determine entity equality by identity.

        Args:
            other: Object to compare.

        Returns:
            True if other is an Entity instance with matching identity id.
        """
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Return hash value based strictly on entity identity id."""
        return hash(self.id)


@dataclass(eq=False)
class AggregateRoot(Entity):
    """Base class for Domain-Driven Design Aggregate Roots.

    Encapsulates a boundary of domain entities and manages uncommitted
    domain events produced during state transitions.
    """

    _domain_events: list[DomainEvent] = field(
        default_factory=list, init=False, repr=False
    )

    @property
    def domain_events(self) -> tuple[DomainEvent, ...]:
        """Return an immutable sequence of uncommitted domain events."""
        return tuple(self._domain_events)

    def register_event(self, event: DomainEvent) -> None:
        """Register a new uncommitted domain event.

        Args:
            event: Domain event to queue.
        """
        self._domain_events.append(event)

    def remove_event(self, event: DomainEvent) -> bool:
        """Remove a specific uncommitted domain event if present.

        Args:
            event: Domain event instance to remove.

        Returns:
            True if event was removed, False otherwise.
        """
        if event in self._domain_events:
            self._domain_events.remove(event)
            return True
        return False

    def clear_events(self) -> list[DomainEvent]:
        """Clear and return all uncommitted domain events.

        Returns:
            List of uncommitted domain events that were cleared.
        """
        events = list(self._domain_events)
        self._domain_events.clear()
        return events
