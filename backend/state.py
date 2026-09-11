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
        "status": "started"
    }