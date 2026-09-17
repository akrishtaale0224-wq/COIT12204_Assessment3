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

    assert result == (
        "Available study hours must be greater than zero."
    )


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

    assert result["error_count"] == 0
    assert result["history"][0]["action"] == "agent_started"
    assert result["history"][1]["action"] == (
        "agent_execution_started"
    )
    assert result["history"][-1]["action"] == (
        "agent_execution_completed"
    )


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
    assert result["error_count"] == 1
    assert result["agent_response"] == (
        "I was unable to process your request. "
        "Please try again."
    )

    assert result["history"][-1]["action"] == (
        "agent_execution_failed"
    )

    assert result["history"][-1]["status"] == "failed"


def test_run_agent_mocked_llm_success(monkeypatch):

    class MockAIMessage:

        content = "A mock response for testing."

        tool_calls = []


    def mock_agent_invoke(*args, **kwargs):

        return {
            "messages": [
                MockAIMessage()
            ]
        }


    monkeypatch.setattr(
        "backend.agent.agent.invoke",
        mock_agent_invoke
    )

    result = run_agent(
        "Explain APIs."
    )

    assert result["status"] == "completed"
    assert result["agent_response"] == (
        "A mock response for testing."
    )
    assert result["tool_used"] is False
    assert result["error_count"] == 0


def test_run_agent_mocked_llm_failure(monkeypatch):

    def mock_agent_failure(*args, **kwargs):

        raise RuntimeError(
            "Mocked LLM connection failure"
        )


    monkeypatch.setattr(
        "backend.agent.agent.invoke",
        mock_agent_failure
    )

    result = run_agent(
        "Explain APIs."
    )

    assert result["status"] == "failed"
    assert result["error_count"] == 1

    assert result["agent_response"] == (
        "I was unable to process your request. "
        "Please try again."
    )


def test_run_agent_records_tool_call(monkeypatch):

    class MockAIMessage:

        content = "Here is your study plan."

        tool_calls = [
            {
                "name": "create_study_plan"
            }
        ]


    def mock_agent_invoke(*args, **kwargs):

        return {
            "messages": [
                MockAIMessage()
            ]
        }


    monkeypatch.setattr(
        "backend.agent.agent.invoke",
        mock_agent_invoke
    )

    result = run_agent(
        "Create a study plan."
    )

    assert result["status"] == "completed"
    assert result["tool_used"] is True
    assert result["last_tool_call"] == (
        "create_study_plan"
    )

    assert any(
        item["action"] == "tool_called"
        for item in result["history"]
    )

def test_run_agent_logs_state_transition(monkeypatch, caplog):

    class MockAIMessage:

        content = "Mock logging response."

        tool_calls = []


    def mock_agent_invoke(*args, **kwargs):

        return {
            "messages": [
                MockAIMessage()
            ]
        }


    monkeypatch.setattr(
        "backend.agent.agent.invoke",
        mock_agent_invoke
    )

    with caplog.at_level("INFO"):

        result = run_agent(
            "Test logging."
        )

    assert result["status"] == "completed"

    assert (
        "State transition: started -> running"
        in caplog.text
    )

    assert (
        "State transition: running -> completed"
        in caplog.text
    )