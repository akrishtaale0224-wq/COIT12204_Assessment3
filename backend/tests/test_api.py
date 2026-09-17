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


def test_agent_endpoint_handles_agent_failure(monkeypatch):

    def mock_failed_agent(message):

        return {
            "status": "failed",
            "agent_response": (
                "I was unable to process your request. "
                "Please try again."
            ),
            "tool_used": False
        }

    monkeypatch.setattr(
        "backend.main.run_agent",
        mock_failed_agent
    )

    response = client.post(
        "/api/agent",
        json={
            "message": "Test agent failure."
        }
    )

    assert response.status_code == 500

    data = response.json()

    assert data["detail"] == (
        "Agent was unable to process the request."
    )


def test_agent_endpoint_handles_unexpected_error(monkeypatch):

    def mock_unexpected_error(message):

        raise RuntimeError(
            "Unexpected test error"
        )

    monkeypatch.setattr(
        "backend.main.run_agent",
        mock_unexpected_error
    )

    response = client.post(
        "/api/agent",
        json={
            "message": "Test unexpected failure."
        }
    )

    assert response.status_code == 500

    data = response.json()

    assert data["detail"] == (
        "Unable to process the agent request."
    )