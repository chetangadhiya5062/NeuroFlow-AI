"""Unit and API tests for Knowledge Base subsystem."""

import tempfile

import pytest
from fastapi.testclient import TestClient

from backend.api.app import get_application
from backend.knowledge_base import (
    InMemoryKnowledgeBaseRepository,
    KnowledgeBaseService,
    LocalFileStorage,
)


@pytest.mark.asyncio
async def test_knowledge_base_ingestion_and_retrieval() -> None:
    """Test document format validation, local file storage, and metadata retrieval."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo = InMemoryKnowledgeBaseRepository()
        storage = LocalFileStorage(base_directory=tmp_dir)
        service = KnowledgeBaseService(repository=repo, storage=storage)

        content = b"Sample text content for testing."
        res = await service.ingest_document(
            filename="test_doc.txt",
            content=content,
            content_type="text/plain",
        )
        assert res.is_success
        doc = res.unwrap()

        assert doc.metadata.filename == "test_doc.txt"
        assert doc.metadata.mime_type == "text/plain"
        assert doc.metadata.file_extension == ".txt"
        assert doc.metadata.size_bytes == len(content)

        # Retrieve doc by ID
        get_res = await service.get_document(doc.id)
        assert get_res.is_success
        assert get_res.unwrap().id == doc.id


@pytest.mark.asyncio
async def test_unsupported_format_raises_error() -> None:
    """Test uploading an unsupported format (e.g. .exe) fails validation."""
    service = KnowledgeBaseService(repository=InMemoryKnowledgeBaseRepository())
    res = await service.ingest_document(
        filename="malicious.exe",
        content=b"executable binary data",
    )
    assert not res.is_success
    err = res.unwrap_err()
    assert err.error_code == "UNSUPPORTED_DOCUMENT_FORMAT"


def test_documents_api_upload_and_list() -> None:
    """Test POST /documents/upload and GET /documents endpoints."""
    app = get_application()
    client = TestClient(app)

    # 1. Upload Markdown file
    response = client.post(
        "/documents/upload",
        files={"file": ("report.md", b"# Report Title\nContent", "text/markdown")},
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["metadata"]["filename"] == "report.md"
    assert data["metadata"]["mime_type"] == "text/markdown"
    doc_id = data["id"]

    # 2. Get document by ID
    get_resp = client.get(f"/documents/{doc_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == doc_id

    # 3. List documents
    list_resp = client.get("/documents")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1
