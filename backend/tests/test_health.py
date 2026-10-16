import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Smart Peel AI" in data["message"]
    assert "version" in data
    assert "docs_url" in data
    assert "health_check" in data


def test_health_check_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Smart Peel AI"
    assert data["version"] == "1.0.0"
    assert "checks" in data
    assert data["checks"]["api"] == "ok"


def test_root_health_alias():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
