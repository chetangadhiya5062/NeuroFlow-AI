"""Integration tests for POST /chat end-to-end AI request flow."""

from fastapi.testclient import TestClient


def test_post_chat_success(client: TestClient) -> None:
    """Test POST /chat returns 200 OK with mock response text."""
    payload = {"message": "Hello NeuroFlow AI"}
    response = client.post("/chat", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Hello from NeuroFlow AI Mock Provider"


def test_post_chat_empty_message_returns_400_bad_request(
    client: TestClient,
) -> None:
    """Test POST /chat with empty message string returns 400 Bad Request."""
    payload = {"message": ""}
    response = client.post("/chat", json=payload)

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "cannot be empty" in data["detail"]
