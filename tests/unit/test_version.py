"""Unit tests for system version endpoint."""

from fastapi.testclient import TestClient


def test_version_endpoint_returns_200_ok(client: TestClient) -> None:
    """Test GET /version returns 200 OK with expected version details."""
    response = client.get("/version")
    assert response.status_code == 200

    data = response.json()
    assert data["app_name"] == "NeuroFlow AI"
    assert data["version"] == "0.1.0"
    assert data["environment"] == "development"
    assert "debug" in data
