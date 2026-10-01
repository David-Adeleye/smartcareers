"""Tests for the operational health endpoint."""

from fastapi.testclient import TestClient

from smartcareers_api.main import app

client = TestClient(app)


def test_health_returns_service_metadata() -> None:
    """The health endpoint should return the configured service information."""

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "SmartCareers API",
        "version": "0.1.0",
        "environment": "development",
    }
