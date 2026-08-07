"""Platform Domain Subsystem for NeuroFlow AI."""

from backend.platform_domain.exceptions import (
    PlatformDomainError,
    ProjectNotFoundError,
    UserNotFoundError,
    WorkspaceNotFoundError,
)
from backend.platform_domain.project import Project
from backend.platform_domain.repositories import (
    InMemoryProjectRepository,
    InMemoryUserRepository,
    InMemoryWorkspaceRepository,
    IProjectRepository,
    IUserRepository,
    IWorkspaceRepository,
)
from backend.platform_domain.service import PlatformDomainService
from backend.platform_domain.user import User
from backend.platform_domain.workspace import Workspace

__all__ = [
    "IProjectRepository",
    "IUserRepository",
    "IWorkspaceRepository",
    "InMemoryProjectRepository",
    "InMemoryUserRepository",
    "InMemoryWorkspaceRepository",
    "PlatformDomainError",
    "PlatformDomainService",
    "Project",
    "ProjectNotFoundError",
    "User",
    "UserNotFoundError",
    "Workspace",
    "WorkspaceNotFoundError",
]
