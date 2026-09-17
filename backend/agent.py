import logging

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

from .config import GEMINI_API_KEY
from .state import create_initial_state, update_state


logger = logging.getLogger(__name__)


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to the .env file."
    )


# Explicit prompt template used by the agent.
PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are StudyMate AI, a university study assistant.

Your role is to help students understand academic and
technical concepts clearly.

Guidelines:
- Explain concepts using simple language.
- Provide examples when useful.
- Help students learn rather than simply giving unexplained answers.
- Be respectful and professional.
- Keep responses clear and organised.
- If you are uncertain, say so.
- Do not claim to have accessed information that you cannot access.

You have access to a study planning tool.

Use the study planning tool when the student asks for
help creating a study plan or organising study time.

When using the study planning tool:
- Identify the subject.
- Identify the available study hours.
- Use the tool result in your final answer.

Always provide a clear final response to the student.
"""
        ),
        (
            "human",
            "{input}"
        )
    ]
)


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
    system_prompt=PROMPT_TEMPLATE.messages[0].prompt.template
)


def extract_agent_response(messages):
    """
    Extract the final text response from the agent messages.
    """

    for message in reversed(messages):

        content = getattr(message, "content", "")

        if isinstance(content, str) and content.strip():
            return content

        if isinstance(content, list):

            text = "".join(
                item.get("text", "")
                for item in content
                if isinstance(item, dict)
                and item.get("text")
            )

            if text.strip():
                return text

    return ""


def run_agent(user_message: str):
    """
    Run the StudyMate single agent and return its internal state.
    """

    if not user_message or not user_message.strip():
        raise ValueError(
            "User message cannot be empty."
        )

    clean_message = user_message.strip()

    state = create_initial_state(clean_message)

    state["conversation_history"].append(
        {
            "role": "user",
            "content": clean_message
        }
    )

    update_state(
        state,
        "running",
        "agent_execution_started"
    )

    logger.info(
        "State transition: started -> running"
    )

    try:

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": clean_message
                    }
                ]
            }
        )

        messages = result.get(
            "messages",
            []
        )

        if not messages:
            raise ValueError(
                "Agent returned no messages."
            )

        response = extract_agent_response(
            messages
        )

        if not response:
            raise ValueError(
                "Agent returned an empty response."
            )

        # Check whether the agent used a tool.
        tool_used = False
        last_tool_call = ""

        for message in messages:

            tool_calls = getattr(
                message,
                "tool_calls",
                None
            )

            if tool_calls:

                tool_used = True

                first_tool = tool_calls[0]

                last_tool_call = first_tool.get(
                    "name",
                    ""
                )

                break

        state["agent_response"] = response
        state["tool_used"] = tool_used
        state["last_tool_call"] = last_tool_call

        state["conversation_history"].append(
            {
                "role": "assistant",
                "content": response
            }
        )

        if tool_used:

            state["history"].append(
                {
                    "action": "tool_called",
                    "status": "running"
                }
            )

            logger.info(
                "State transition: tool_called (%s)",
                last_tool_call
            )

        update_state(
            state,
            "completed",
            "agent_execution_completed"
        )

        logger.info(
            "State transition: running -> completed"
        )

        return state

    except Exception as error:

        state["error_count"] += 1

        state["status"] = "failed"

        state["agent_response"] = (
            "I was unable to process your request. "
            "Please try again."
        )

        state["history"].append(
            {
                "action": "agent_execution_failed",
                "status": "failed"
            }
        )

        logger.error(
            "State transition: running -> failed. Error: %s",
            repr(error)
        )

        return state