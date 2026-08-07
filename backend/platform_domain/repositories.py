"""Repositories for User, Workspace, and Project platform entities."""

import threading
from abc import ABC, abstractmethod

from backend.core.value_objects import EntityId
from backend.platform_domain.project import Project
from backend.platform_domain.user import User
from backend.platform_domain.workspace import Workspace


class IUserRepository(ABC):
    """Abstract port interface for User entity persistence."""

    @abstractmethod
    async def save(self, user: User) -> None:
        """Save or update user entity."""

    @abstractmethod
    async def get_by_id(self, user_id: EntityId) -> User | None:
        """Get user entity by EntityId."""


class InMemoryUserRepository(IUserRepository):
    """Thread-safe in-memory repository for User entities."""

    def __init__(self) -> None:
        """Initialize lock and store."""
        self._lock = threading.RLock()
        self._users: dict[str, User] = {}

    async def save(self, user: User) -> None:
        """Save user in memory."""
        with self._lock:
            self._users[user.id.value] = user

    async def get_by_id(self, user_id: EntityId) -> User | None:
        """Get user by ID."""
        with self._lock:
            return self._users.get(user_id.value)


class IWorkspaceRepository(ABC):
    """Abstract port interface for Workspace entity persistence."""

    @abstractmethod
    async def save(self, workspace: Workspace) -> None:
        """Save or update workspace entity."""

    @abstractmethod
    async def get_by_id(self, workspace_id: EntityId) -> Workspace | None:
        """Get workspace entity by EntityId."""


class InMemoryWorkspaceRepository(IWorkspaceRepository):
    """Thread-safe in-memory repository for Workspace entities."""

    def __init__(self) -> None:
        """Initialize lock and store."""
        self._lock = threading.RLock()
        self._workspaces: dict[str, Workspace] = {}

    async def save(self, workspace: Workspace) -> None:
        """Save workspace in memory."""
        with self._lock:
            self._workspaces[workspace.id.value] = workspace

    async def get_by_id(self, workspace_id: EntityId) -> Workspace | None:
        """Get workspace by ID."""
        with self._lock:
            return self._workspaces.get(workspace_id.value)


class IProjectRepository(ABC):
    """Abstract port interface for Project entity persistence."""

    @abstractmethod
    async def save(self, project: Project) -> None:
        """Save or update project entity."""

    @abstractmethod
    async def get_by_id(self, project_id: EntityId) -> Project | None:
        """Get project entity by EntityId."""

    @abstractmethod
    async def list_by_workspace(self, workspace_id: EntityId) -> list[Project]:
        """List all projects under a workspace."""


class InMemoryProjectRepository(IProjectRepository):
    """Thread-safe in-memory repository for Project entities."""

    def __init__(self) -> None:
        """Initialize lock and store."""
        self._lock = threading.RLock()
        self._projects: dict[str, Project] = {}

    async def save(self, project: Project) -> None:
        """Save project in memory."""
        with self._lock:
            self._projects[project.id.value] = project

    async def get_by_id(self, project_id: EntityId) -> Project | None:
        """Get project by ID."""
        with self._lock:
            return self._projects.get(project_id.value)

    async def list_by_workspace(self, workspace_id: EntityId) -> list[Project]:
        """List projects belonging to workspace."""
        with self._lock:
            return [
                p
                for p in self._projects.values()
                if p.workspace_id.value == workspace_id.value
            ]
