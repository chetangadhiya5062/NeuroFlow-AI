"""API routes for multi-tenant platform domain entities."""

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pydantic import BaseModel

from backend.api.routes.documents import DocumentResponse
from backend.config import get_container
from backend.platform_domain import PlatformDomainService

router = APIRouter(tags=["Platform Domain"])


class CreateWorkspaceRequest(BaseModel):
    """API request payload for creating a Workspace."""

    name: str
    owner_id: str | None = None


class WorkspaceResponse(BaseModel):
    """API response payload for a Workspace."""

    id: str
    name: str
    owner_id: str
    tenant_id: str
    created_at: str


class CreateProjectRequest(BaseModel):
    """API request payload for creating a Project."""

    name: str
    description: str | None = None


class ProjectResponse(BaseModel):
    """API response payload for a Project."""

    id: str
    workspace_id: str
    name: str
    description: str | None = None
    created_at: str


class ConversationSummaryResponse(BaseModel):
    """API response model for a Project conversation summary."""

    id: str
    title: str | None = None
    message_count: int
    created_at: str
    updated_at: str


@router.post(
    "/workspaces",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_workspace(
    request: CreateWorkspaceRequest,
) -> WorkspaceResponse:
    """Create a new multi-tenant Workspace."""
    container = get_container()
    service = container.resolve(PlatformDomainService)

    owner_id = request.owner_id or "01912a3b-4c5d-7e8f-9a0b-1c2d3e4f5a6b"
    result = await service.create_workspace(
        name=request.name, owner_id=owner_id
    )

    if not result.is_success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.unwrap_err().message,
        )

    ws = result.unwrap()
    return WorkspaceResponse(
        id=ws.id.value,
        name=ws.name,
        owner_id=ws.owner_id.value,
        tenant_id=ws.tenant_id.value,
        created_at=ws.created_at.value.isoformat(),
    )


@router.post(
    "/workspaces/{workspace_id}/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    workspace_id: str, request: CreateProjectRequest
) -> ProjectResponse:
    """Create a new Project inside a Workspace."""
    container = get_container()
    service = container.resolve(PlatformDomainService)

    result = await service.create_project(
        workspace_id=workspace_id,
        name=request.name,
        description=request.description,
    )

    if not result.is_success:
        err = result.unwrap_err()
        status_code = (
            status.HTTP_404_NOT_FOUND
            if err.error_code == "WORKSPACE_NOT_FOUND"
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=err.message)

    proj = result.unwrap()
    return ProjectResponse(
        id=proj.id.value,
        workspace_id=proj.workspace_id.value,
        name=proj.name,
        description=proj.description,
        created_at=proj.created_at.value.isoformat(),
    )


@router.get(
    "/workspaces/{workspace_id}/projects",
    response_model=list[ProjectResponse],
)
async def list_projects(workspace_id: str) -> list[ProjectResponse]:
    """List all projects belonging to a Workspace."""
    container = get_container()
    service = container.resolve(PlatformDomainService)

    result = await service.list_projects(workspace_id=workspace_id)
    if not result.is_success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.unwrap_err().message,
        )

    projects = result.unwrap()
    return [
        ProjectResponse(
            id=p.id.value,
            workspace_id=p.workspace_id.value,
            name=p.name,
            description=p.description,
            created_at=p.created_at.value.isoformat(),
        )
        for p in projects
    ]


@router.get(
    "/projects/{project_id}/conversations",
    response_model=list[ConversationSummaryResponse],
)
async def list_project_conversations(
    project_id: str,
) -> list[ConversationSummaryResponse]:
    """List conversations stored inside a Project."""
    container = get_container()
    service = container.resolve(PlatformDomainService)

    result = await service.list_project_conversations(project_id=project_id)
    if not result.is_success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.unwrap_err().message,
        )

    conversations = result.unwrap()
    return [
        ConversationSummaryResponse(
            id=c.id.value,
            title=c.title,
            message_count=len(c.messages),
            created_at=c.created_at.value.isoformat(),
            updated_at=c.updated_at.value.isoformat(),
        )
        for c in conversations
    ]


@router.post(
    "/projects/{project_id}/documents/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_project_document(
    project_id: str,
    file: UploadFile = File(...),  # noqa: B008
) -> DocumentResponse:
    """Upload and ingest a document into a Project."""
    container = get_container()
    service = container.resolve(PlatformDomainService)

    content = await file.read()
    filename = file.filename or "file.txt"

    result = await service.upload_project_document(
        project_id=project_id,
        filename=filename,
        content=content,
        content_type=file.content_type,
    )

    if not result.is_success:
        err = result.unwrap_err()
        status_code = (
            status.HTTP_404_NOT_FOUND
            if err.error_code == "PROJECT_NOT_FOUND"
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=status_code, detail=err.message)

    doc = result.unwrap()
    from backend.api.routes.documents import DocumentMetadataResponse

    return DocumentResponse(
        id=doc.id.value,
        storage_path=doc.storage_path,
        metadata=DocumentMetadataResponse(
            filename=doc.metadata.filename,
            size_bytes=doc.metadata.size_bytes,
            mime_type=doc.metadata.mime_type,
            file_extension=doc.metadata.file_extension,
            checksum=doc.metadata.checksum,
            uploaded_at=doc.metadata.uploaded_at.value.isoformat(),
            created_at=doc.metadata.created_at.value.isoformat(),
        ),
    )
