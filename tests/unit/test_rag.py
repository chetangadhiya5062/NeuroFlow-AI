"""Unit and vertical slice integration tests for RAG Subsystem."""

import tempfile

import pytest
from fastapi.testclient import TestClient

from backend.api.app import get_application
from backend.knowledge_base import (
    InMemoryKnowledgeBaseRepository,
    KnowledgeBaseService,
    LocalFileStorage,
)
from backend.rag import RAGService


@pytest.mark.asyncio
async def test_rag_ingest_and_retrieve_vertical_slice() -> None:
    """Test full RAG vertical slice: Document Ingestion -> Chunking -> Vector Search."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        rag_service = RAGService()
        kb_repo = InMemoryKnowledgeBaseRepository()
        storage = LocalFileStorage(base_directory=tmp_dir)

        service = KnowledgeBaseService(
            repository=kb_repo, storage=storage, rag_service=rag_service
        )

        doc_content = (
            b"# NeuroFlow AI Platform\n"
            b"NeuroFlow AI engine supporting high throughput retrieval "
            b"and vector storage using normalized cosine similarity embeddings."
        )

        # 1. Ingest document via KnowledgeBaseService
        ingest_res = await service.ingest_document(
            filename="report.md",
            content=doc_content,
            content_type="text/markdown",
        )
        assert ingest_res.is_success
        doc = ingest_res.unwrap()
        assert doc.metadata.filename == "report.md"

        # 2. Retrieve relevant context chunks via RAGService
        query = "What similarity metric does NeuroFlow AI use for vector storage?"
        ret_res = await rag_service.retrieve_context(query, top_k=2)
        assert ret_res.is_success
        matches = ret_res.unwrap()

        assert len(matches) >= 1
        assert matches[0].record.metadata["filename"] == "report.md"
        assert "cosine similarity" in matches[0].record.text

        # 3. Format sources for downstream LLM prompt runtime
        sources = rag_service.format_sources(matches)
        assert len(sources) >= 1
        assert sources[0]["filename"] == "report.md"
        assert "similarity_score" in sources[0]


def test_rag_chat_api_vertical_slice() -> None:
    """Test complete RAG API flow: Upload document -> POST /chat."""
    app = get_application()
    client = TestClient(app)

    # 1. Upload Knowledge Document
    upload_resp = client.post(
        "/documents/upload",
        files={
            "file": (
                "spec.md",
                (
                    b"# NeuroFlow Specification\n"
                    b"NeuroFlow AI includes a production-grade LLM Gateway."
                ),
                "text/markdown",
            )
        },
    )
    assert upload_resp.status_code == 201

    # 2. Ask question via POST /chat
    chat_resp = client.post(
        "/chat",
        json={"message": "What does NeuroFlow specification include?"},
    )
    assert chat_resp.status_code == 200
    data = chat_resp.json()
    assert "response" in data
    assert "sources" in data
    assert len(data["sources"]) >= 1
    assert any(s["filename"] == "spec.md" for s in data["sources"])
