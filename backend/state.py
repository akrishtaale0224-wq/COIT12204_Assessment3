from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict, total=False):
    """
    Internal state used by the StudyMate AI single agent.
    """

    user_message: str

    conversation_history: List[Dict[str, str]]

    agent_response: str

    tool_used: bool

    tool_result: Any

    last_tool_call: str

    error_count: int

    history: List[Dict[str, str]]

    status: str


def create_initial_state(user_message: str) -> AgentState:
    """
    Create the initial state for an agent request.
    """

    return {
        "user_message": user_message,
        "conversation_history": [],
        "agent_response": "",
        "tool_used": False,
        "tool_result": None,
        "last_tool_call": "",
        "error_count": 0,
        "history": [
            {
                "action": "agent_started",
                "status": "started"
            }
        ],
        "status": "started"
    }


def update_state(
    state: AgentState,
    status: str,
    action: str
) -> AgentState:
    """
    Update the agent state and record a state transition.
    """

    state["status"] = status

    state["history"].append(
        {
            "action": action,
            "status": status
        }
    )

    return state