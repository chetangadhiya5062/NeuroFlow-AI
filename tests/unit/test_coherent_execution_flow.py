"""End-to-end integration tests for Coherent Platform Execution Flow."""

from fastapi.testclient import TestClient

from backend.api.app import get_application


def test_path_1_tool_invocation_flow() -> None:
    """Test Path 1: Tool Execution Path (What is 945 × 82?)."""  # noqa: RUF002
    app = get_application()
    client = TestClient(app)

    response = client.post(
        "/chat",
        json={"message": "What is 945 × 82?"},  # noqa: RUF001
    )
    assert response.status_code == 200
    data = response.json()

    assert "response" in data
    assert "77,490" in data["response"] or "77490" in data["response"]


def test_path_2_knowledge_retrieval_flow() -> None:
    """Test Path 2: Knowledge Retrieval Path (Uploaded PDF RRC Setup)."""
    app = get_application()
    client = TestClient(app)

    # 1. Upload Knowledge Document
    doc_content = (
        b"# Telecom Architecture\n"
        b"Radio Resource Control (RRC) Setup establishes initial RRC connection "
        b"between User Equipment (UE) and gNodeB base station in 5G NR networks."
    )
    upload_resp = client.post(
        "/documents/upload",
        files={
            "file": (
                "telecom.pdf",
                doc_content,
                "application/pdf",
            )
        },
    )
    assert upload_resp.status_code == 201

    # 2. Query Knowledge Base via Chat Endpoint
    response = client.post(
        "/chat",
        json={"message": "What does the uploaded PDF say about RRC Setup?"},
    )
    assert response.status_code == 200
    data = response.json()

    assert "response" in data
    assert "sources" in data
    assert len(data["sources"]) >= 1
    assert data["sources"][0]["filename"] == "telecom.pdf"


def test_path_3_direct_conversation_flow() -> None:
    """Test Path 3: Direct Conversation Path (Hello)."""
    app = get_application()
    client = TestClient(app)

    response = client.post(
        "/chat",
        json={"message": "Hello"},
    )
    assert response.status_code == 200
    data = response.json()

    assert "response" in data
    assert len(data["response"]) > 0
