"""End-to-end user capability test: Chat with Your Documents."""

from fastapi.testclient import TestClient

from backend.api.app import get_application


def test_chat_with_documents_vertical_slice() -> None:
    """Demonstrate the complete 12-step 'Chat with Your Documents' workflow."""
    app = get_application()
    client = TestClient(app)

    # Step 1-6: Upload document (telecom.pdf)
    document_content = (
        b"# Telecom Architecture Overview\n"
        b"Radio Resource Control (RRC) Setup establishes initial RRC connection "
        b"between User Equipment (UE) and gNodeB base station in 5G NR networks."
    )

    upload_response = client.post(
        "/documents/upload",
        files={
            "file": (
                "telecom.pdf",
                document_content,
                "application/pdf",
            )
        },
    )

    assert upload_response.status_code == 201
    upload_data = upload_response.json()

    assert "id" in upload_data
    assert upload_data["metadata"]["filename"] == "telecom.pdf"
    assert upload_data["metadata"]["file_extension"] == ".pdf"

    # Step 7-12: Ask question -> Retrieve -> Assemble prompt -> Call LLM -> Return
    chat_response = client.post(
        "/chat",
        json={"message": "What is the purpose of RRC Setup?"},
    )

    assert chat_response.status_code == 200
    chat_data = chat_response.json()

    # 11. Answer returned
    assert "response" in chat_data
    assert len(chat_data["response"]) > 0

    # 12. Sources displayed with filename citations
    assert "sources" in chat_data
    assert len(chat_data["sources"]) >= 1

    matched_source = chat_data["sources"][0]
    assert matched_source["filename"] == "telecom.pdf"
    assert "gNodeB base station" in matched_source["text"]
