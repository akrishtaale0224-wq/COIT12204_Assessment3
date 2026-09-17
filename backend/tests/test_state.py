from backend.state import create_initial_state


def test_create_initial_state():

    state = create_initial_state(
        "Help me study Java."
    )

    assert state["user_message"] == "Help me study Java."
    assert state["conversation_history"] == []
    assert state["agent_response"] == ""
    assert state["tool_used"] is False
    assert state["tool_result"] is None
    assert state["status"] == "started"