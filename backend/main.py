import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .chatbot import generate_response
from .security import sanitise_message
from .agent import run_agent


# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="StudyMate AI API",
    description="Backend API for the StudyMate AI chatbot and single agent",
    version="2.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )


# Conversation history for the current application session
conversation_history = []


@app.get("/api/health")
def health_check():

    return {
        "status": "healthy",
        "service": "StudyMate AI"
    }


@app.post("/api/chat/new")
def new_chat():

    conversation_history.clear()

    logger.info("New conversation started.")

    return {
        "message": "New conversation started."
    }


@app.post("/api/chat")
def chat(request: ChatRequest):

    try:

        # Sanitise the user's message
        clean_message = sanitise_message(request.message)

        logger.info("Chat request received.")

        # Add the user's message to conversation history
        conversation_history.append(
            {
                "role": "user",
                "content": clean_message
            }
        )

        # Send the complete conversation to Gemini
        response = generate_response(
            conversation_history
        )

        # Add the AI response to conversation history
        conversation_history.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        logger.info("Chat response generated successfully.")

        return {
            "response": response
        }

    except Exception as error:

        logger.error(
            "LLM API error: %s",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to generate a response."
        )


@app.post("/api/agent")
def agent_chat(request: ChatRequest):

    try:

        # Sanitise the user's message before sending it to the agent
        clean_message = sanitise_message(request.message)

        logger.info("Agent request received.")

        # Run the LangChain single agent
        result = run_agent(clean_message)

        # Check whether the agent completed successfully
        if result["status"] != "completed":

            logger.error(
                "Agent execution failed: %s",
                result["agent_response"]
            )

            raise HTTPException(
                status_code=500,
                detail="Agent was unable to process the request."
            )

        logger.info(
            "Agent completed successfully. Tool used: %s",
            result["tool_used"]
        )

        return {
            "response": result["agent_response"],
            "tool_used": result["tool_used"],
            "status": result["status"]
        }

    except HTTPException:

        raise

    except Exception as error:

        logger.error(
            "Unexpected agent error: %s",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to process the agent request."
        )