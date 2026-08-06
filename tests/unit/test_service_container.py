"""Unit tests for thread-safe Dependency Injection container framework."""

from abc import ABC, abstractmethod

import pytest

from backend.config import ServiceContainer
from backend.core.exceptions import ConfigurationError


class DummyInterface(ABC):
    """Abstract interface for testing container resolution."""

    @abstractmethod
    def execute(self) -> str:
        """Abstract execution method."""


class DummyService(DummyInterface):
    """Concrete implementation for testing container resolution."""

    def execute(self) -> str:
        """Return dummy status."""
        return "SUCCESS"


def test_service_container_singleton_registration() -> None:
    """Test registering and resolving a pre-constructed singleton instance."""
    container = ServiceContainer()
    instance = DummyService()

    container.register_singleton(
        DummyInterface, instance=instance  # type: ignore[type-abstract]
    )

    assert container.is_registered(DummyInterface)
    resolved = container.resolve(DummyInterface)
    assert resolved is instance
    assert resolved.execute() == "SUCCESS"


def test_service_container_lazy_singleton_factory() -> None:
    """Test registering and resolving a lazy singleton factory."""
    container = ServiceContainer()
    calls = 0

    def factory(c: ServiceContainer) -> DummyService:
        nonlocal calls
        calls += 1
        return DummyService()

    container.register_singleton(
        DummyInterface, factory=factory  # type: ignore[type-abstract]
    )

    assert container.is_registered(DummyInterface)
    first = container.resolve(DummyInterface)
    second = container.resolve(DummyInterface)

    assert first is second
    assert calls == 1


def test_service_container_transient_registration() -> None:
    """Test registering and resolving transient instances."""
    container = ServiceContainer()

    container.register_transient(
        DummyInterface,
        factory=lambda c: DummyService(),  # type: ignore[type-abstract]
    )

    first = container.resolve(DummyInterface)
    second = container.resolve(DummyInterface)

    assert first is not second
    assert isinstance(first, DummyService)
    assert isinstance(second, DummyService)


def test_service_container_unregistered_raises_error() -> None:
    """Test resolving an unregistered interface raises ConfigurationError."""
    container = ServiceContainer()

    with pytest.raises(ConfigurationError, match="No registration found"):
        container.resolve(DummyInterface)


def test_service_container_clear() -> None:
    """Test clearing container resets all registrations."""
    container = ServiceContainer()
    container.register_singleton(
        DummyInterface, instance=DummyService()  # type: ignore[type-abstract]
    )

    assert container.is_registered(DummyInterface)
    container.clear()
    assert not container.is_registered(DummyInterface)
