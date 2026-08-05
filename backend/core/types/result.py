"""Monadic Result types for explicit success/failure handling in NeuroFlow AI."""

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class ErrorInfo:
    """Structured immutable container for error metadata.

    Attributes:
        message: Human-readable error description.
        error_code: Unique uppercase error identifier.
        details: Additional context dictionary.
        retryable: Indicates if the operation may be retried.
        timestamp: ISO 8601 UTC timestamp of error occurrence.
    """

    message: str
    error_code: str = "ERROR"
    details: dict[str, Any] = field(default_factory=dict)
    retryable: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass(frozen=True)
class Success[T]:
    """Represents a successful operation outcome containing a value of type T.

    Attributes:
        value: The success payload value.
    """

    value: T

    @property
    def is_success(self) -> bool:
        """Return True if the result is a Success."""
        return True

    @property
    def is_failure(self) -> bool:
        """Return False if the result is a Success."""
        return False

    def unwrap(self) -> T:
        """Unwrap and return the success value."""
        return self.value

    def unwrap_or(self, default: Any) -> T:
        """Return the success value, ignoring the default.

        Args:
            default: Ignored fallback value.

        Returns:
            The contained success value.
        """
        return self.value

    def unwrap_err(self) -> Any:
        """Raise ValueError as Success has no error payload."""
        raise ValueError("Called unwrap_err on a Success result.")

    def map[U](self, fn: Callable[[T], U]) -> "Success[U]":
        """Apply fn to the contained value and return a new Success instance.

        Args:
            fn: Transformation function to apply to value.

        Returns:
            New Success instance containing transformed value.
        """
        return Success(fn(self.value))

    def flat_map[U](self, fn: Callable[[T], "Result[U, Any]"]) -> "Result[U, Any]":
        """Apply fn returning a Result to the contained value.

        Args:
            fn: Function returning a Result.

        Returns:
            Result returned by fn.
        """
        return fn(self.value)

    def on_success(self, fn: Callable[[T], None]) -> "Success[T]":
        """Execute side-effect callback with value and return self.

        Args:
            fn: Callback function to execute with value.

        Returns:
            Self.
        """
        fn(self.value)
        return self

    def on_failure(self, fn: Callable[[Any], None]) -> "Success[T]":
        """Ignore failure callback and return self.

        Args:
            fn: Ignored callback function.

        Returns:
            Self.
        """
        return self


@dataclass(frozen=True)
class Failure[E]:
    """Represents a failed operation outcome containing an error payload of type E.

    Attributes:
        error: The error payload (e.g., ErrorInfo or Exception).
    """

    error: E

    @property
    def is_success(self) -> bool:
        """Return False if the result is a Failure."""
        return False

    @property
    def is_failure(self) -> bool:
        """Return True if the result is a Failure."""
        return True

    def unwrap(self) -> Any:
        """Raise Exception or ValueError containing the error payload."""
        if isinstance(self.error, Exception):
            raise self.error
        raise ValueError(f"Result is a Failure: {self.error}")

    def unwrap_or[U](self, default: U) -> U:
        """Return the default fallback value since result is a Failure.

        Args:
            default: Fallback value to return.

        Returns:
            The provided default value.
        """
        return default

    def unwrap_err(self) -> E:
        """Unwrap and return the error payload."""
        return self.error

    def map(self, fn: Callable[[Any], Any]) -> "Failure[E]":
        """Ignore mapping on Failure and return self.

        Args:
            fn: Ignored transformation function.

        Returns:
            Self.
        """
        return self

    def flat_map(self, fn: Callable[[Any], "Result[Any, Any]"]) -> "Failure[E]":
        """Ignore flat_map on Failure and return self.

        Args:
            fn: Ignored transformation function.

        Returns:
            Self.
        """
        return self

    def on_success(self, fn: Callable[[Any], None]) -> "Failure[E]":
        """Ignore success callback and return self.

        Args:
            fn: Ignored callback function.

        Returns:
            Self.
        """
        return self

    def on_failure(self, fn: Callable[[E], None]) -> "Failure[E]":
        """Execute side-effect callback with error payload and return self.

        Args:
            fn: Callback function to execute with error.

        Returns:
            Self.
        """
        fn(self.error)
        return self


# Monadic Result Type Alias (Python 3.12 type statement)
type Result[T, E] = Success[T] | Failure[E]


def Ok[T](value: T) -> Success[T]:  # noqa: N802
    """Construct a Success result containing a value.

    Args:
        value: The success payload value.

    Returns:
        Success instance wrapper.
    """
    return Success(value)


def Err[E](error: E) -> Failure[E]:  # noqa: N802
    """Construct a Failure result containing an error payload.

    Args:
        error: The error payload.

    Returns:
        Failure instance wrapper.
    """
    return Failure(error)
