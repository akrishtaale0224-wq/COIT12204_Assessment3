from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

from .config import GEMINI_API_KEY


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to the .env file."
    )


SYSTEM_PROMPT = """
You are StudyMate AI, a university study assistant.

Your role is to help students understand academic and technical
concepts clearly.

Guidelines:
- Explain concepts using simple language.
- Provide examples when useful.
- Help students learn rather than simply giving unexplained answers.
- Be respectful and professional.
- Keep responses clear and organised.
- If you are uncertain, say so.
- Do not claim to have accessed information that you cannot access.

You have access to a study planning tool.

Use the study planning tool when the student asks for help
creating a study plan or organising study time.
"""


@tool
def create_study_plan(subject: str, available_hours: int) -> str:
    """
    Create a simple study plan for a university subject.
    """

    if available_hours <= 0:
        return "Available study hours must be greater than zero."

    if available_hours == 1:
        return (
            f"For {subject}, use your 1 hour for: "
            "20 minutes reviewing concepts, "
            "25 minutes practising questions, and "
            "15 minutes reviewing mistakes."
        )

    if available_hours == 2:
        return (
            f"For {subject}, use your 2 hours for: "
            "45 minutes learning concepts, "
            "45 minutes practising questions, and "
            "30 minutes reviewing mistakes."
        )

    return (
        f"For {subject}, use your {available_hours} available hours for: "
        "1 hour reviewing concepts, "
        "1 hour practising questions, "
        "30 minutes reviewing mistakes, and "
        "the remaining time revising difficult topics."
    )


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2
)


agent = create_agent(
    model=model,
    tools=[create_study_plan],
    system_prompt=SYSTEM_PROMPT
)


def run_agent(user_message: str):
    """
    Run the StudyMate agent and return its internal state.
    """

    if not user_message or not user_message.strip():
        raise ValueError("User message cannot be empty.")

    from .state import create_initial_state

    state = create_initial_state(user_message.strip())

    state["conversation_history"].append(
        {
            "role": "user",
            "content": user_message.strip()
        }
    )

    try:
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_message.strip()
                    }
                ]
            }
        )

        messages = result.get("messages", [])

        if not messages:
            raise ValueError("Agent returned no messages.")

        # Find the final AI response.
        response = ""

        for message in reversed(messages):
            content = getattr(message, "content", "")

            if isinstance(content, str) and content.strip():
                response = content
                break

            if isinstance(content, list):
                text = "".join(
                    item.get("text", "")
                    for item in content
                    if isinstance(item, dict)
                    and item.get("text")
                )

                if text.strip():
                    response = text
                    break

        if not response:
            raise ValueError("Agent returned an empty response.")

        # Record whether a tool call occurred.
        tool_used = False

        for message in messages:
            tool_calls = getattr(message, "tool_calls", None)

            if tool_calls:
                tool_used = True
                break

        state["agent_response"] = response
        state["tool_used"] = tool_used
        state["status"] = "completed"

        state["conversation_history"].append(
            {
                "role": "assistant",
                "content": response
            }
        )

        return state

    except Exception as error:

        state["status"] = "failed"
        state["agent_response"] = str(error)

        return state