from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health_endpoint():

    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "StudyMate AI"


def test_agent_endpoint_rejects_empty_message():

    response = client.post(
        "/api/agent",
        json={
            "message": ""
        }
    )

    assert response.status_code == 422


def test_agent_endpoint_accepts_valid_message():

    response = client.post(
        "/api/agent",
        json={
            "message": "Explain what an API is in simple terms."
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data
    assert data["status"] == "completed"
    assert isinstance(data["tool_used"], bool)


def test_agent_endpoint_rejects_message_over_2000_characters():

    long_message = "A" * 2001

    response = client.post(
        "/api/agent",
        json={
            "message": long_message
        }
    )

    assert response.status_code == 422


def test_new_chat_endpoint():

    response = client.post("/api/chat/new")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "New conversation started."