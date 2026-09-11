from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .chatbot import generate_response
from .security import sanitise_message


app = FastAPI(
    title="StudyMate AI API",
    description="Backend API for the StudyMate AI chatbot",
    version="1.0.0"
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

    return {
        "message": "New conversation started."
    }


@app.post("/api/chat")
def chat(request: ChatRequest):

    try:

        # Sanitise the user's message
        clean_message = sanitise_message(request.message)

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

        return {
            "response": response
        }

    except Exception as error:

        print("=" * 60)
        print("LLM API ERROR:")
        print(repr(error))
        print("=" * 60)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )