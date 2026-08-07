"""User domain entity definition."""

from dataclasses import dataclass, field

from backend.core.entities import AggregateRoot
from backend.core.value_objects import EntityId, Timestamp


@dataclass
class User(AggregateRoot):
    """User entity representing a platform user account.

    Attributes:
        id: Unique EntityId for user.
        email: User email address string.
        name: User display name string.
        created_at: User creation Timestamp.
    """

    email: str = ""
    name: str = ""
    id: EntityId = field(default_factory=EntityId)
    created_at: Timestamp = field(default_factory=Timestamp)

    @classmethod
    def create(cls, email: str, name: str) -> "User":
        """Factory method constructing a new User instance.

        Args:
            email: User email address.
            name: User full display name.

        Returns:
            Instantiated User aggregate root.
        """
        return cls(
            id=EntityId(),
            email=email,
            name=name,
            created_at=Timestamp(),
        )
