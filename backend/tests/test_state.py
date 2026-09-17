from backend.state import create_initial_state, update_state


def test_create_initial_state():

    state = create_initial_state(
        "Help me study Java."
    )

    assert state["user_message"] == "Help me study Java."
    assert state["conversation_history"] == []
    assert state["agent_response"] == ""
    assert state["tool_used"] is False
    assert state["tool_result"] is None

    # Check additional state variables
    assert state["last_tool_call"] == ""
    assert state["error_count"] == 0
    assert state["status"] == "started"

    # Check initial state history
    assert len(state["history"]) == 1
    assert state["history"][0]["action"] == "agent_started"
    assert state["history"][0]["status"] == "started"


def test_state_transition():

    state = create_initial_state(
        "Create a study plan."
    )

    update_state(
        state,
        "running",
        "agent_execution_started"
    )

    assert state["status"] == "running"

    assert len(state["history"]) == 2

    assert state["history"][1]["action"] == (
        "agent_execution_started"
    )

    assert state["history"][1]["status"] == "running"


def test_state_records_multiple_transitions():

    state = create_initial_state(
        "Help me study."
    )

    update_state(
        state,
        "running",
        "agent_execution_started"
    )

    update_state(
        state,
        "completed",
        "agent_execution_completed"
    )

    assert state["status"] == "completed"
    assert len(state["history"]) == 3

    assert state["history"][2]["action"] == (
        "agent_execution_completed"
    )

    assert state["history"][2]["status"] == "completed"