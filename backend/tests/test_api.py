import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_chat_endpoint_exists():
    # Test that the chat endpoint is available (though it will likely fail due to missing API keys)
    response = client.post("/api/chat", json={"query": "test"})
    # Should return 422 (validation error) or 400 (validation error) rather than 404 (not found)
    assert response.status_code in [400, 422, 401, 500]