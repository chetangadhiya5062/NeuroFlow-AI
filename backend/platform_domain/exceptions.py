"""Platform domain subsystem exception definitions."""

from typing import Any

from backend.core.exceptions import PlatformError


class PlatformDomainError(PlatformError):
    """Base exception for all Platform Domain errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "PLATFORM_DOMAIN_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize PlatformDomainError."""
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
        )


class UserNotFoundError(PlatformDomainError):
    """Raised when a requested user entity is not found."""

    def __init__(
        self,
        user_id: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize UserNotFoundError."""
        super().__init__(
            message=f"User '{user_id}' was not found.",
            error_code="USER_NOT_FOUND",
            details=details,
        )


class WorkspaceNotFoundError(PlatformDomainError):
    """Raised when a requested workspace entity is not found."""

    def __init__(
        self,
        workspace_id: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize WorkspaceNotFoundError."""
        super().__init__(
            message=f"Workspace '{workspace_id}' was not found.",
            error_code="WORKSPACE_NOT_FOUND",
            details=details,
        )


class ProjectNotFoundError(PlatformDomainError):
    """Raised when a requested project entity is not found."""

    def __init__(
        self,
        project_id: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ProjectNotFoundError."""
        super().__init__(
            message=f"Project '{project_id}' was not found.",
            error_code="PROJECT_NOT_FOUND",
            details=details,
        )
