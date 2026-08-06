"""Unit tests for system health check endpoint."""

from fastapi.testclient import TestClient


def test_health_endpoint_returns_200_ok(client: TestClient) -> None:
    """Test GET /health returns 200 OK with expected payload structure."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["app"] == "NeuroFlow AI"
    assert "version" in data
    assert "environment" in data
