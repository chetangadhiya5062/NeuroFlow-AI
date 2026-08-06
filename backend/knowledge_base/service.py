"""Knowledge Base domain service orchestrating document ingestion and retrieval."""

import hashlib

from backend.core.types import Err, ErrorInfo, Ok, Result
from backend.core.value_objects import EntityId, TenantId, Timestamp
from backend.knowledge_base.document import Document
from backend.knowledge_base.exceptions import KnowledgeBaseError
from backend.knowledge_base.metadata import DocumentMetadata
from backend.knowledge_base.parser import DocumentParser
from backend.knowledge_base.repository import IKnowledgeBaseRepository
from backend.knowledge_base.storage import LocalFileStorage


class KnowledgeBaseService:
    """Service managing document ingestion, file storage, and metadata lifecycle."""

    def __init__(
        self,
        repository: IKnowledgeBaseRepository,
        storage: LocalFileStorage | None = None,
        parser: DocumentParser | None = None,
    ) -> None:
        """Initialize KnowledgeBaseService with repository and storage dependencies."""
        self._repository = repository
        self._storage = storage or LocalFileStorage()
        self._parser = parser or DocumentParser()

    async def ingest_document(
        self,
        filename: str,
        content: bytes,
        content_type: str | None = None,
        tenant_id: TenantId | None = None,
    ) -> Result[Document, ErrorInfo]:
        """Ingest, validate, store, and record metadata for a document file.

        Args:
            filename: Original file name.
            content: Raw document byte content.
            content_type: Optional MIME content-type string.
            tenant_id: Optional TenantId.

        Returns:
            Result wrapping persisted Document or ErrorInfo.
        """
        try:
            # 1. Validate format (PDF, TXT, MD)
            ext, mime_type = self._parser.validate_format(filename, content_type)

            # 2. Compute metadata properties
            size_bytes = len(content)
            checksum = hashlib.sha256(content).hexdigest()
            doc_id = EntityId()

            # 3. Store raw file locally in data/documents/
            storage_path = await self._storage.save_file(
                document_id=doc_id.value,
                filename=filename,
                content=content,
            )

            # 4. Construct DocumentMetadata and Document aggregate
            metadata = DocumentMetadata(
                filename=filename,
                size_bytes=size_bytes,
                mime_type=mime_type,
                file_extension=ext,
                checksum=checksum,
                uploaded_at=Timestamp(),
                created_at=Timestamp(),
            )
            document = Document(
                id=doc_id,
                storage_path=storage_path,
                metadata=metadata,
                tenant_id=tenant_id,
            )

            # 5. Persist Document metadata in repository
            await self._repository.save(document)
            return Ok(document)
        except KnowledgeBaseError as exc:
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
                    message=f"Document ingestion failed: {exc}",
                    error_code="DOCUMENT_INGESTION_ERROR",
                )
            )

    async def get_document(
        self, document_id: EntityId | str
    ) -> Result[Document, ErrorInfo]:
        """Retrieve document aggregate by EntityId or string ID.

        Args:
            document_id: EntityId or string ID.

        Returns:
            Result wrapping Document or ErrorInfo if not found.
        """
        did = (
            document_id
            if isinstance(document_id, EntityId)
            else EntityId(document_id)
        )
        doc = await self._repository.get_by_id(did)
        if doc is None:
            return Err(
                ErrorInfo(
                    message=f"Document '{did.value}' was not found.",
                    error_code="DOCUMENT_NOT_FOUND",
                )
            )
        return Ok(doc)

    async def list_documents(
        self, tenant_id: TenantId | None = None, limit: int = 50
    ) -> Result[list[Document], ErrorInfo]:
        """List stored documents up to limit.

        Args:
            tenant_id: Optional TenantId.
            limit: Maximum document count.

        Returns:
            Result wrapping list of Document aggregates.
        """
        docs = await self._repository.list_documents(tenant_id, limit)
        return Ok(docs)

    async def delete_document(
        self, document_id: EntityId | str
    ) -> Result[bool, ErrorInfo]:
        """Delete document metadata and local file by document ID."""
        get_res = await self.get_document(document_id)
        if not get_res.is_success:
            return Err(get_res.unwrap_err())

        doc = get_res.unwrap()
        await self._storage.delete_file(doc.storage_path)
        deleted = await self._repository.delete(doc.id)
        return Ok(deleted)
