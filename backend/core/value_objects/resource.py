"""Resource value objects for file paths, URIs, and token budgets."""

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from backend.core.exceptions import ValidationError


@dataclass(frozen=True)
class FilePath:
    """Immutable filesystem path value object.

    Attributes:
        value: Path instance representing a valid file or directory path.
    """

    value: Path | str

    def __post_init__(self) -> None:
        """Validate path instance or convert string to Path."""
        if isinstance(self.value, str):
            if not self.value.strip():
                raise ValidationError("FilePath value must be non-empty.")
            object.__setattr__(self, "value", Path(self.value))
        elif isinstance(self.value, Path):
            object.__setattr__(self, "value", self.value)
        else:
            raise ValidationError("FilePath value must be a Path or str instance.")

    def __str__(self) -> str:
        """Return string path representation."""
        return str(self.value)


@dataclass(frozen=True)
class Uri:
    """Immutable URI / URL value object.

    Attributes:
        value: Valid URI or URL string.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate URI string format and scheme presence."""
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValidationError("Uri value must be a non-empty string.")

        parsed = urlparse(self.value)
        if not parsed.scheme:
            raise ValidationError(
                f"Uri '{self.value}' must contain a valid scheme."
            )

    @property
    def scheme(self) -> str:
        """Return the URI scheme."""
        return urlparse(self.value).scheme

    def __str__(self) -> str:
        """Return string representation of Uri."""
        return self.value


@dataclass(frozen=True)
class TokenBudget:
    """Immutable LLM token budget allocation and usage tracker.

    Attributes:
        allocated: Maximum allowed token budget (must be > 0).
        used: Token quantity consumed so far (must be >= 0).
    """

    allocated: int
    used: int = 0

    def __post_init__(self) -> None:
        """Validate token budget invariants."""
        if not isinstance(self.allocated, int) or self.allocated <= 0:
            raise ValidationError(
                "TokenBudget allocated must be a positive integer."
            )
        if not isinstance(self.used, int) or self.used < 0:
            raise ValidationError(
                "TokenBudget used must be a non-negative integer."
            )
        if self.used > self.allocated:
            raise ValidationError(
                f"TokenBudget used ({self.used}) > allocated ({self.allocated})."
            )

    @property
    def remaining(self) -> int:
        """Return remaining unconsumed tokens."""
        return self.allocated - self.used

    @property
    def is_exhausted(self) -> bool:
        """Return True if no tokens remain."""
        return self.remaining <= 0

    def consume(self, count: int) -> "TokenBudget":
        """Return a new TokenBudget instance with consumed tokens added to used count.

        Args:
            count: Number of tokens to consume.

        Returns:
            New TokenBudget instance.

        Raises:
            ValidationError: If count is non-positive or exceeds remaining.
        """
        if not isinstance(count, int) or count <= 0:
            raise ValidationError("Consumed token count must be a positive integer.")
        if count > self.remaining:
            raise ValidationError(
                f"Cannot consume {count} tokens; only {self.remaining} remaining."
            )
        return TokenBudget(allocated=self.allocated, used=self.used + count)
