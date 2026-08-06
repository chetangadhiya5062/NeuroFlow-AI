"""Foundation abstract port contracts for logging, config, storage, and bus."""

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any

from backend.core.events import DomainEvent
from backend.core.value_objects import EntityId, FilePath, Timestamp, Uri


class ILogger(ABC):
    """Abstract port interface for platform logging."""

    @abstractmethod
    def debug(self, msg: str, **kwargs: Any) -> None:
        """Log a debug message."""

    @abstractmethod
    def info(self, msg: str, **kwargs: Any) -> None:
        """Log an informational message."""

    @abstractmethod
    def warning(self, msg: str, **kwargs: Any) -> None:
        """Log a warning message."""

    @abstractmethod
    def error(self, msg: str, **kwargs: Any) -> None:
        """Log an error message."""

    @abstractmethod
    def critical(self, msg: str, **kwargs: Any) -> None:
        """Log a critical failure message."""


class IConfigurationProvider(ABC):
    """Abstract port interface for environment and platform configuration."""

    @abstractmethod
    def get[T](self, key: str, default: T | None = None) -> T | None:
        """Retrieve a configuration value by key."""

    @abstractmethod
    def has(self, key: str) -> bool:
        """Check if a configuration key exists."""


class IClock(ABC):
    """Abstract port interface for system time generation."""

    @abstractmethod
    def now(self) -> Timestamp:
        """Return the current timezone-aware UTC Timestamp."""


class IIdGenerator(ABC):
    """Abstract port interface for unique identifier generation."""

    @abstractmethod
    def generate(self) -> EntityId:
        """Generate a new unique EntityId."""


class IStorageProvider(ABC):
    """Abstract port interface for blob and object storage providers."""

    @abstractmethod
    async def save(self, path: FilePath, data: bytes) -> Uri:
        """Save binary data to storage and return its Uri location."""

    @abstractmethod
    async def read(self, uri: Uri) -> bytes:
        """Read binary data from storage by Uri."""

    @abstractmethod
    async def delete(self, uri: Uri) -> bool:
        """Delete object from storage by Uri."""

    @abstractmethod
    async def exists(self, uri: Uri) -> bool:
        """Check if object exists in storage by Uri."""


class ICacheStore(ABC):
    """Abstract port interface for key-value caching adapters."""

    @abstractmethod
    async def get(self, key: str) -> Any | None:
        """Retrieve cached value by key."""

    @abstractmethod
    async def set(
        self, key: str, value: Any, ttl_seconds: int | None = None
    ) -> None:
        """Set cached value with optional expiration time in seconds."""

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete cached entry by key."""

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if cached key exists."""


class IMessageQueue(ABC):
    """Abstract port interface for task queues and async message brokers."""

    @abstractmethod
    async def enqueue(self, topic: str, payload: dict[str, Any]) -> None:
        """Enqueue message payload onto topic."""

    @abstractmethod
    async def dequeue(self, topic: str) -> dict[str, Any] | None:
        """Dequeue next available message payload from topic."""


class IEventBus(ABC):
    """Abstract port interface for internal domain event bus."""

    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        """Publish domain event to subscribers."""

    @abstractmethod
    async def subscribe(
        self,
        event_type: type[DomainEvent],
        handler: Callable[[DomainEvent], Awaitable[None]],
    ) -> None:
        """Subscribe handler function to domain event type."""
