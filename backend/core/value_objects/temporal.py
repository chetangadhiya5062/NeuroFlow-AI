"""Temporal value objects for event and audit timestamps."""

from dataclasses import dataclass, field
from datetime import UTC, datetime

from backend.core.exceptions import ValidationError


@dataclass(frozen=True)
class Timestamp:
    """Immutable timezone-aware UTC timestamp value object.

    Attributes:
        value: datetime instance forced to UTC timezone.
    """

    value: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        """Ensure the timestamp value is timezone-aware and converted to UTC."""
        if not isinstance(self.value, datetime):
            raise ValidationError("Timestamp value must be a datetime instance.")

        if self.value.tzinfo is None:
            # Force naive datetime to UTC
            object.__setattr__(self, "value", self.value.replace(tzinfo=UTC))
        elif self.value.tzinfo != UTC:
            object.__setattr__(self, "value", self.value.astimezone(UTC))

    @classmethod
    def from_isoformat(cls, iso_str: str) -> "Timestamp":
        """Construct Timestamp from ISO 8601 string.

        Args:
            iso_str: ISO formatted timestamp string.

        Returns:
            Timestamp instance.
        """
        try:
            dt = datetime.fromisoformat(iso_str)
            return cls(dt)
        except Exception as exc:
            raise ValidationError(
                f"Invalid ISO timestamp string: '{iso_str}'."
            ) from exc

    def to_isoformat(self) -> str:
        """Return ISO 8601 string representation."""
        return self.value.isoformat()

    def __str__(self) -> str:
        """Return string ISO representation."""
        return self.to_isoformat()
