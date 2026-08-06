"""Identifier value objects for entities, tenants, traces, and models."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from backend.core.exceptions import ValidationError


@dataclass(frozen=True)
class EntityId:
    """Immutable unique identifier for domain entities.

    Attributes:
        value: String representation of a UUID.
    """

    value: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        """Validate that value is a non-empty string and valid UUID format."""
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValidationError("EntityId value must be a non-empty string.")
        try:
            UUID(self.value)
        except ValueError as exc:
            raise ValidationError(
                f"EntityId '{self.value}' is not a valid UUID."
            ) from exc

    def __str__(self) -> str:
        """Return the string value of the EntityId."""
        return self.value


@dataclass(frozen=True)
class TenantId:
    """Immutable multi-tenant identifier establishing tenant isolation.

    Attributes:
        value: Non-empty string tenant identifier.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate that tenant ID is a non-empty string."""
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValidationError("TenantId value must be a non-empty string.")

    def __str__(self) -> str:
        """Return string representation of TenantId."""
        return self.value


@dataclass(frozen=True)
class CorrelationId:
    """Immutable correlation identifier for cross-service request tracking.

    Attributes:
        value: String correlation identifier.
    """

    value: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        """Validate that correlation ID is a non-empty string."""
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValidationError(
                "CorrelationId value must be a non-empty string."
            )

    def __str__(self) -> str:
        """Return string representation of CorrelationId."""
        return self.value


@dataclass(frozen=True)
class TraceId:
    """Immutable distributed tracing identifier for OpenTelemetry contexts.

    Attributes:
        value: Hexadecimal string or UUID trace identifier.
    """

    value: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        """Validate that trace ID is a non-empty string."""
        if not isinstance(self.value, str) or not self.value.strip():
            raise ValidationError("TraceId value must be a non-empty string.")

    def __str__(self) -> str:
        """Return string representation of TraceId."""
        return self.value


@dataclass(frozen=True)
class ModelIdentifier:
    """Immutable AI model specification identifier.

    Attributes:
        name: Name or model string (e.g., 'gpt-4o', 'claude-3-5-sonnet').
        provider: Provider identifier (e.g., 'openai', 'anthropic', 'ollama').
    """

    name: str
    provider: str = "openai"

    def __post_init__(self) -> None:
        """Validate that model name and provider are non-empty strings."""
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValidationError("Model name must be a non-empty string.")
        if not isinstance(self.provider, str) or not self.provider.strip():
            raise ValidationError("Model provider must be a non-empty string.")

    @property
    def canonical_name(self) -> str:
        """Return the formatted provider/model canonical string."""
        return f"{self.provider.lower()}/{self.name.lower()}"

    def __str__(self) -> str:
        """Return canonical name representation."""
        return self.canonical_name
