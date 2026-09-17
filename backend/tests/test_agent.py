from backend.agent import create_study_plan, run_agent


def test_create_study_plan_one_hour():

    result = create_study_plan.invoke(
        {
            "subject": "Java",
            "available_hours": 1
        }
    )

    assert "Java" in result
    assert "20 minutes" in result


def test_create_study_plan_two_hours():

    result = create_study_plan.invoke(
        {
            "subject": "Java",
            "available_hours": 2
        }
    )

    assert "Java" in result
    assert "2 hours" in result
    assert "45 minutes" in result


def test_create_study_plan_invalid_hours():

    result = create_study_plan.invoke(
        {
            "subject": "Java",
            "available_hours": 0
        }
    )

    assert result == "Available study hours must be greater than zero."


def test_run_agent_creates_completed_state():

    result = run_agent(
        "Explain what an API is in simple terms."
    )

    assert result["status"] == "completed"
    assert result["user_message"] == (
        "Explain what an API is in simple terms."
    )
    assert result["agent_response"]
    assert len(result["conversation_history"]) == 2
    assert result["conversation_history"][0]["role"] == "user"
    assert result["conversation_history"][1]["role"] == "assistant"


def test_run_agent_rejects_empty_message():

    try:
        run_agent("")
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == "User message cannot be empty."


def test_run_agent_rejects_whitespace_message():

    try:
        run_agent("   ")
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == "User message cannot be empty."

def test_run_agent_handles_agent_failure(monkeypatch):

    def failing_agent(*args, **kwargs):
        raise RuntimeError("Test agent failure")

    monkeypatch.setattr(
        "backend.agent.agent.invoke",
        failing_agent
    )

    result = run_agent(
        "Test failure handling."
    )

    assert result["status"] == "failed"
    assert "Test agent failure" in result["agent_response"]