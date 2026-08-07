"""Platform Domain Service managing Workspace and Project hierarchies."""

from backend.conversation import Conversation, ConversationService
from backend.core.types import Err, ErrorInfo, Ok, Result
from backend.core.value_objects import EntityId, TenantId
from backend.knowledge_base import Document, KnowledgeBaseService
from backend.platform_domain.exceptions import PlatformDomainError
from backend.platform_domain.project import Project
from backend.platform_domain.repositories import (
    InMemoryProjectRepository,
    InMemoryUserRepository,
    InMemoryWorkspaceRepository,
    IProjectRepository,
    IUserRepository,
    IWorkspaceRepository,
)
from backend.platform_domain.user import User
from backend.platform_domain.workspace import Workspace


class PlatformDomainService:
    """Master domain service managing User -> Workspace -> Project hierarchy."""

    def __init__(
        self,
        user_repo: IUserRepository | None = None,
        workspace_repo: IWorkspaceRepository | None = None,
        project_repo: IProjectRepository | None = None,
        conversation_service: ConversationService | None = None,
        knowledge_service: KnowledgeBaseService | None = None,
    ) -> None:
        """Initialize PlatformDomainService with repository dependencies."""
        self.user_repo = user_repo or InMemoryUserRepository()
        self.workspace_repo = workspace_repo or InMemoryWorkspaceRepository()
        self.project_repo = project_repo or InMemoryProjectRepository()
        self.conversation_service = conversation_service
        self.knowledge_service = knowledge_service

    async def create_user(
        self, email: str, name: str
    ) -> Result[User, ErrorInfo]:
        """Create and persist a new User entity."""
        try:
            user = User.create(email=email, name=name)
            await self.user_repo.save(user)
            return Ok(user)
        except Exception as exc:
            return Err(
                ErrorInfo(
                    message=f"Failed to create user: {exc}",
                    error_code="USER_CREATION_ERROR",
                )
            )

    async def create_workspace(
        self, name: str, owner_id: str | EntityId
    ) -> Result[Workspace, ErrorInfo]:
        """Create and persist a new Workspace for owner user.

        Args:
            name: Workspace name string.
            owner_id: EntityId or string ID of owner.

        Returns:
            Result wrapping created Workspace aggregate.
        """
        try:
            oid = (
                owner_id
                if isinstance(owner_id, EntityId)
                else EntityId(owner_id)
            )
            user = await self.user_repo.get_by_id(oid)
            if user is None:
                # Create user if absent for seamless multi-tenant demo
                user = User(
                    id=oid, email="owner@neuroflow.ai", name="Workspace Owner"
                )
                await self.user_repo.save(user)

            workspace = Workspace.create(name=name, owner_id=user.id)
            await self.workspace_repo.save(workspace)
            return Ok(workspace)
        except PlatformDomainError as exc:
            return Err(
                ErrorInfo(
                    message=exc.message,
                    error_code=exc.error_code,
                    details=exc.details,
                )
            )
        except Exception as exc:
            return Err(
                ErrorInfo(
                    message=f"Failed to create workspace: {exc}",
                    error_code="WORKSPACE_CREATION_ERROR",
                )
            )

    async def get_workspace(
        self, workspace_id: str | EntityId
    ) -> Result[Workspace, ErrorInfo]:
        """Get Workspace by EntityId or string ID."""
        wid = (
            workspace_id
            if isinstance(workspace_id, EntityId)
            else EntityId(workspace_id)
        )
        ws = await self.workspace_repo.get_by_id(wid)
        if ws is None:
            return Err(
                ErrorInfo(
                    message=f"Workspace '{wid.value}' was not found.",
                    error_code="WORKSPACE_NOT_FOUND",
                )
            )
        return Ok(ws)

    async def create_project(
        self,
        workspace_id: str | EntityId,
        name: str,
        description: str | None = None,
    ) -> Result[Project, ErrorInfo]:
        """Create a new Project within a Workspace.

        Args:
            workspace_id: EntityId or string ID of target Workspace.
            name: Project name string.
            description: Optional description.

        Returns:
            Result wrapping created Project aggregate.
        """
        ws_res = await self.get_workspace(workspace_id)
        if not ws_res.is_success:
            return Err(ws_res.unwrap_err())

        ws = ws_res.unwrap()
        project = Project.create(
            workspace_id=ws.id, name=name, description=description
        )
        await self.project_repo.save(project)
        return Ok(project)

    async def get_project(
        self, project_id: str | EntityId
    ) -> Result[Project, ErrorInfo]:
        """Get Project by EntityId or string ID."""
        pid = (
            project_id
            if isinstance(project_id, EntityId)
            else EntityId(project_id)
        )
        proj = await self.project_repo.get_by_id(pid)
        if proj is None:
            return Err(
                ErrorInfo(
                    message=f"Project '{pid.value}' was not found.",
                    error_code="PROJECT_NOT_FOUND",
                )
            )
        return Ok(proj)

    async def list_projects(
        self, workspace_id: str | EntityId
    ) -> Result[list[Project], ErrorInfo]:
        """List projects belonging to workspace."""
        wid = (
            workspace_id
            if isinstance(workspace_id, EntityId)
            else EntityId(workspace_id)
        )
        projects = await self.project_repo.list_by_workspace(wid)
        return Ok(projects)

    async def list_project_conversations(
        self, project_id: str | EntityId
    ) -> Result[list[Conversation], ErrorInfo]:
        """List conversations stored inside project."""
        if self.conversation_service is None:
            return Ok([])

        pid = (
            project_id
            if isinstance(project_id, EntityId)
            else EntityId(project_id)
        )
        # Fetch conversations filtered by project_id
        all_convs = (
            await self.conversation_service._repository.list_conversations()
        )
        project_convs = [
            c
            for c in all_convs
            if c.project_id and c.project_id.value == pid.value
        ]
        return Ok(project_convs)

    async def upload_project_document(
        self,
        project_id: str | EntityId,
        filename: str,
        content: bytes,
        content_type: str | None = None,
    ) -> Result[Document, ErrorInfo]:
        """Ingest document attached to project and parent workspace."""
        if self.knowledge_service is None:
            return Err(
                ErrorInfo(
                    message="KnowledgeBaseService is not registered.",
                    error_code="SERVICE_UNAVAILABLE",
                )
            )

        proj_res = await self.get_project(project_id)
        if not proj_res.is_success:
            return Err(proj_res.unwrap_err())

        proj = proj_res.unwrap()
        tenant_id = TenantId(proj.workspace_id.value)

        ingest_res = await self.knowledge_service.ingest_document(
            filename=filename,
            content=content,
            content_type=content_type,
            tenant_id=tenant_id,
        )

        if ingest_res.is_success:
            doc = ingest_res.unwrap()
            doc.project_id = proj.id
            doc.workspace_id = proj.workspace_id
            return Ok(doc)

        return ingest_res
