"""Thread-safe Dependency Injection container framework for NeuroFlow AI."""

import threading
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from backend.core.exceptions import ConfigurationError


class ServiceLifetime(Enum):
    """Lifetime classification for registered container services."""

    SINGLETON = auto()
    TRANSIENT = auto()
    FACTORY = auto()


@dataclass
class ServiceRegistration[T]:
    """Container service registration definition.

    Attributes:
        interface: Service interface type or key.
        lifetime: Registration lifetime strategy.
        factory: Optional factory function producing instances.
        instance: Cached singleton instance if initialized.
    """

    interface: type[T]
    lifetime: ServiceLifetime
    factory: Callable[["ServiceContainer"], T] | None = None
    instance: T | None = None


class ServiceRegistry:
    """Registry maintaining active service interface registrations."""

    def __init__(self) -> None:
        """Initialize empty service registry."""
        self._registrations: dict[type[Any], ServiceRegistration[Any]] = {}

    def register[T](self, registration: ServiceRegistration[T]) -> None:
        """Register service definition in registry."""
        self._registrations[registration.interface] = registration

    def get[T](self, interface: type[T]) -> ServiceRegistration[T] | None:
        """Retrieve registration for interface if registered."""
        return self._registrations.get(interface)

    def has(self, interface: type[Any]) -> bool:
        """Check if interface is registered."""
        return interface in self._registrations

    def clear(self) -> None:
        """Clear all service registrations."""
        self._registrations.clear()


class DependencyResolver:
    """Resolver constructing and fetching instances from registrations."""

    def __init__(self, container: "ServiceContainer") -> None:
        """Initialize resolver with parent container reference."""
        self._container = container

    def resolve[T](self, registration: ServiceRegistration[T]) -> T:
        """Resolve instance according to service lifetime strategy.

        Args:
            registration: Service registration object to resolve.

        Returns:
            Resolved instance of type T.

        Raises:
            ConfigurationError: If instance or factory is invalid.
        """
        if registration.lifetime == ServiceLifetime.SINGLETON:
            if registration.instance is not None:
                return registration.instance

            if registration.factory is not None:
                instance = registration.factory(self._container)
                registration.instance = instance
                return instance

            raise ConfigurationError(
                f"Singleton registration for '{registration.interface.__name__}' "
                "has no instance or factory."
            )

        if registration.lifetime in (
            ServiceLifetime.TRANSIENT,
            ServiceLifetime.FACTORY,
        ):
            if registration.factory is not None:
                return registration.factory(self._container)
            raise ConfigurationError(
                f"Factory registration for '{registration.interface.__name__}' "
                "has no factory function."
            )

        raise ConfigurationError(
            f"Unsupported lifetime '{registration.lifetime}' "
            f"for '{registration.interface.__name__}'."
        )


class ServiceContainer:
    """Thread-safe Dependency Injection container for NeuroFlow AI."""

    def __init__(self) -> None:
        """Initialize container, lock, registry, and resolver."""
        self._lock = threading.RLock()
        self._registry = ServiceRegistry()
        self._resolver = DependencyResolver(self)

    def register_singleton[T](
        self,
        interface: type[T],
        instance: T | None = None,
        factory: Callable[["ServiceContainer"], T] | None = None,
    ) -> None:
        """Register a service as a thread-safe Singleton.

        Args:
            interface: Service interface type.
            instance: Pre-constructed singleton instance.
            factory: Factory function returning singleton instance.

        Raises:
            ConfigurationError: If neither instance nor factory is provided.
        """
        if instance is None and factory is None:
            raise ConfigurationError(
                f"Cannot register singleton '{interface.__name__}': "
                "must provide either instance or factory."
            )

        with self._lock:
            self._registry.register(
                ServiceRegistration(
                    interface=interface,
                    lifetime=ServiceLifetime.SINGLETON,
                    factory=factory,
                    instance=instance,
                )
            )

    def register_transient[T](
        self,
        interface: type[T],
        factory: Callable[["ServiceContainer"], T],
    ) -> None:
        """Register a service as a Transient factory instance."""
        with self._lock:
            self._registry.register(
                ServiceRegistration(
                    interface=interface,
                    lifetime=ServiceLifetime.TRANSIENT,
                    factory=factory,
                )
            )

    def register_factory[T](
        self,
        interface: type[T],
        factory: Callable[["ServiceContainer"], T],
    ) -> None:
        """Register a factory producing new service instances on each resolve call."""
        with self._lock:
            self._registry.register(
                ServiceRegistration(
                    interface=interface,
                    lifetime=ServiceLifetime.FACTORY,
                    factory=factory,
                )
            )

    def resolve[T](self, interface: type[T]) -> T:
        """Resolve instance for registered interface.

        Args:
            interface: Interface type to resolve.

        Returns:
            Resolved instance of interface T.

        Raises:
            ConfigurationError: If interface is not registered.
        """
        with self._lock:
            registration = self._registry.get(interface)
            if registration is None:
                raise ConfigurationError(
                    f"No registration found for interface '{interface.__name__}'."
                )
            return self._resolver.resolve(registration)

    def is_registered(self, interface: type[Any]) -> bool:
        """Check if an interface is registered in the container."""
        with self._lock:
            return self._registry.has(interface)

    def reset_singletons(self) -> None:
        """Reset cached singleton instances (retaining factories and registrations)."""
        with self._lock:
            for reg in self._registry._registrations.values():
                if (
                    reg.lifetime == ServiceLifetime.SINGLETON
                    and reg.factory is not None
                ):
                    reg.instance = None

    def clear(self) -> None:
        """Clear all service registrations and cached instances."""
        with self._lock:
            self._registry.clear()


_CONTAINER_LOCK = threading.RLock()
_GLOBAL_CONTAINER: ServiceContainer | None = None


def get_container() -> ServiceContainer:
    """Return cached global thread-safe ServiceContainer instance."""
    global _GLOBAL_CONTAINER  # noqa: PLW0603
    with _CONTAINER_LOCK:
        if _GLOBAL_CONTAINER is None:
            _GLOBAL_CONTAINER = ServiceContainer()
        return _GLOBAL_CONTAINER
