"""Unit and end-to-end integration tests for RAG Vertical Slice."""

import tempfile

import pytest
from fastapi.testclient import TestClient

from backend.api.app import get_application
from backend.knowledge_base import (
    InMemoryKnowledgeBaseRepository,
    KnowledgeBaseService,
    LocalFileStorage,
)
from backend.rag import (
    EmbeddingService,
    LocalVectorStorage,
    PDFParser,
    RAGService,
    TextChunker,
)


@pytest.mark.asyncio
async def test_pdf_parser() -> None:
    """Test PDFParser extracts plain text from document bytes."""
    parser = PDFParser()
    txt = parser.parse_document(b"Hello World PDF Content", ".txt")
    assert txt == "Hello World PDF Content"


@pytest.mark.asyncio
async def test_chunker_and_embedding_service() -> None:
    """Test TextChunker splits text and EmbeddingService generates vectors."""
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)
    chunks = chunker.chunk_text(
        document_id="doc-123",
        text=(
            "NeuroFlow AI is a modular intelligent agent platform. "
            "It supports RAG and LLMs."
        ),
    )
    assert len(chunks) >= 1

    embedding_service = EmbeddingService()
    vector = await embedding_service.generate_embedding(chunks[0].text)
    assert len(vector) == 384


@pytest.mark.asyncio
async def test_rag_end_to_end_flow() -> None:
    """Test complete RAG pipeline: document ingestion to retrieval."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        vector_store = LocalVectorStorage()
        rag_service = RAGService(vector_store=vector_store)

        kb_repo = InMemoryKnowledgeBaseRepository()
        storage = LocalFileStorage(base_directory=tmp_dir)
        kb_service = KnowledgeBaseService(
            repository=kb_repo, storage=storage, rag_service=rag_service
        )

        doc_content = (
            b"NeuroFlow AI enables real-time document search "
            b"using vector embeddings."
        )
        ingest_res = await kb_service.ingest_document(
            filename="architecture.txt",
            content=doc_content,
            content_type="text/plain",
        )
        assert ingest_res.is_success

        # Query RAG service for relevant context
        retrieve_res = await rag_service.retrieve_context(
            "What is NeuroFlow AI?", top_k=2
        )
        assert retrieve_res.is_success
        matches = retrieve_res.unwrap()
        assert len(matches) >= 1
        assert "vector embeddings" in matches[0].record.text


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
    assert data["sources"][0]["filename"] == "spec.md"
