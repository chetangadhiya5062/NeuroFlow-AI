"""API routes for Knowledge Base document ingestion and metadata retrieval."""

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status
from pydantic import BaseModel

from backend.config import get_container
from backend.knowledge_base import KnowledgeBaseService

router = APIRouter(prefix="/documents", tags=["Knowledge Base"])


class DocumentMetadataResponse(BaseModel):
    """API response model for document metadata."""

    filename: str
    size_bytes: int
    mime_type: str
    file_extension: str
    checksum: str | None = None
    uploaded_at: str
    created_at: str


class DocumentResponse(BaseModel):
    """API response model for a stored document."""

    id: str
    storage_path: str
    metadata: DocumentMetadataResponse


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),  # noqa: B008
) -> DocumentResponse:
    """Upload and ingest a document file (PDF, TXT, MD)."""
    container = get_container()
    service = container.resolve(KnowledgeBaseService)

    content = await file.read()
    filename = file.filename or "file.txt"

    result = await service.ingest_document(
        filename=filename,
        content=content,
        content_type=file.content_type,
    )

    if not result.is_success:
        err = result.unwrap_err()
        status_code = (
            status.HTTP_400_BAD_REQUEST
            if err.error_code == "UNSUPPORTED_DOCUMENT_FORMAT"
            else status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        raise HTTPException(status_code=status_code, detail=err.message)

    doc = result.unwrap()
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


@router.get("", response_model=list[DocumentResponse])
async def list_documents(
    limit: int = Query(default=50, ge=1, le=200),
) -> list[DocumentResponse]:
    """List ingested knowledge base documents."""
    container = get_container()
    service = container.resolve(KnowledgeBaseService)

    result = await service.list_documents(limit=limit)
    if not result.is_success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.unwrap_err().message,
        )

    docs = result.unwrap()
    return [
        DocumentResponse(
            id=d.id.value,
            storage_path=d.storage_path,
            metadata=DocumentMetadataResponse(
                filename=d.metadata.filename,
                size_bytes=d.metadata.size_bytes,
                mime_type=d.metadata.mime_type,
                file_extension=d.metadata.file_extension,
                checksum=d.metadata.checksum,
                uploaded_at=d.metadata.uploaded_at.value.isoformat(),
                created_at=d.metadata.created_at.value.isoformat(),
            ),
        )
        for d in docs
    ]


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str) -> DocumentResponse:
    """Retrieve document metadata by document ID."""
    container = get_container()
    service = container.resolve(KnowledgeBaseService)

    result = await service.get_document(document_id)
    if not result.is_success:
        err = result.unwrap_err()
        status_code = (
            status.HTTP_404_NOT_FOUND
            if err.error_code == "DOCUMENT_NOT_FOUND"
            else status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        raise HTTPException(status_code=status_code, detail=err.message)

    doc = result.unwrap()
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
