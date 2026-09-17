# StudyMate AI

## COIT12204 – Single Agent Systems

### Assessment 3 – Single-Agent AI System

StudyMate AI is a web-based university study assistant designed to help students understand academic and technical concepts. The application was originally developed as a web-based LLM chatbot and has been extended for Assessment 3 to include a LangChain-based single intelligent agent, internal state management, tool use, FastAPI integration, logging, guardrails and automated testing.

The system uses Google Gemini as the language model and provides a study-planning tool that the agent can use when a student requests help organising study time.

---

## Technologies

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python FastAPI
* **Agent Framework:** LangChain
* **Agent Runtime:** LangGraph through LangChain
* **LLM:** Google Gemini API
* **Testing:** pytest
* **Deployment:** Docker and Render
* **Version Control:** Git and GitHub

---

## Assessment 3 Features

The Assessment 3 version extends the original StudyMate chatbot with the following features:

* LangChain single intelligent agent
* Internal agent state management
* Conversation history within agent state
* Tool calling
* Study-planning tool
* FastAPI agent endpoint
* Input validation
* Message sanitisation
* Controlled error handling
* Application logging
* Automated pytest test suite
* API integration testing
* Agent state testing
* Tool behaviour testing

---

## Single-Agent Architecture

The main Assessment 3 processing flow is:

```text
Student
   ↓
Frontend
   ↓
FastAPI
   ↓
Input Validation
   ↓
Message Sanitisation
   ↓
LangChain Single Agent
   ↓
Google Gemini
   ↓
Tool Selection when required
   ↓
Study Planning Tool
   ↓
Internal Agent State
   ↓
Agent Response
   ↓
FastAPI
   ↓
Frontend
```

The agent is implemented using LangChain's agent framework. Google Gemini provides the language-model reasoning capability, while the study-planning tool provides a controlled action that the agent can call when appropriate.

---

## Internal State

The agent maintains an internal state using the `AgentState` structure in `backend/state.py`.

The state contains:

```text
user_message
conversation_history
agent_response
tool_used
tool_result
status
```

The state begins with a `started` status and is updated when the agent processes the request.

A successful request results in:

```text
status = completed
```

If an exception occurs during agent execution:

```text
status = failed
```

The state also records whether the study-planning tool was used.

---

## Study Planning Tool

The application includes a LangChain tool called:

```text
create_study_plan
```

The tool accepts:

```text
subject
available_hours
```

It generates a simple study plan based on the available study time.

For example, when a student asks:

```text
I have 2 hours to study Java. Create a study plan.
```

the agent can identify that the study-planning tool is appropriate and call it.

The application records:

```text
tool_used = True
```

in the internal agent state.

The tool also validates the available study hours and rejects invalid values such as zero or negative study time.

---

## FastAPI Endpoints

### `/api/health`

Checks whether the StudyMate AI backend is running.

Example response:

```json
{
    "status": "healthy",
    "service": "StudyMate AI"
}
```

### `/api/chat`

The original chatbot endpoint from the StudyMate AI foundation.

It accepts a user message, sanitises the input, maintains conversation history and sends the conversation to Google Gemini.

### `/api/chat/new`

Clears the current chatbot conversation history and starts a new conversation.

### `/api/agent`

The main Assessment 3 endpoint.

It accepts a student message and sends it to the LangChain single agent.

Example request:

```json
{
    "message": "I have 2 hours to study Java. Create a study plan."
}
```

Example response structure:

```json
{
    "response": "Here is a focused study plan...",
    "tool_used": true,
    "status": "completed"
}
```

---

## Guardrails and Validation

The application includes several validation and safety mechanisms.

### Input validation

FastAPI validates incoming messages using Pydantic.

Messages must contain:

* At least 1 character
* No more than 2,000 characters

Invalid requests are rejected by the API before being processed by the agent.

### Message sanitisation

User messages are passed through the existing sanitisation function before being processed.

### Tool validation

The study-planning tool checks that the number of available study hours is greater than zero.

### Controlled errors

Agent failures are caught and represented using the internal state:

```text
status = failed
```

The API also returns controlled HTTP errors rather than exposing internal implementation details to users.

### API key protection

The Gemini API key is stored in an environment variable and is not included in frontend code.

---

## Logging

Python's `logging` module is used by the FastAPI application to record important application events.

Examples include:

```text
Agent request received
Agent completed successfully
Tool used
Chat response generated successfully
Agent execution failed
```

Sensitive information such as API keys is not logged.

Logging provides useful information for debugging and monitoring the application during development.

---

## Testing

The project uses `pytest` for automated testing.

The test suite covers:

* Internal state creation
* Study-planning tool behaviour
* Valid study-planning inputs
* Invalid study-planning inputs
* Agent execution
* Agent internal state after execution
* Empty agent messages
* Whitespace-only messages
* FastAPI health endpoint
* Empty API messages
* Messages exceeding 2,000 characters
* Valid agent API requests
* New-chat endpoint
* Agent failure handling

The current test suite contains:

```text
21 automated tests covering agent behaviour, state transitions, tool behaviour, API validation, mocked LLM responses, failure handling, and logging.
```

All tests were successfully executed during development.

Tests are located in:

```text
backend/tests/
├── test_state.py
├── test_agent.py
└── test_api.py
```

Run the complete test suite using:

```bash
venv\Scripts\python.exe -m pytest backend\tests -v
```

---

## Project Structure

```text
COIT12204_Assessment3/
│
├── backend/
│   ├── tests/
│   │   ├── test_state.py
│   │   ├── test_agent.py
│   │   └── test_api.py
│   │
│   ├── agent.py
│   ├── chatbot.py
│   ├── config.py
│   ├── main.py
│   ├── security.py
│   ├── state.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── __init__.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── .env
├── .gitignore
├── README.md
└── render.yaml
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/akrishtaale0224-wq/COIT12204_Assessment3.git
cd COIT12204_Assessment3
```

### 2. Create and activate the virtual environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r backend\requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file containing:

```text
GEMINI_API_KEY=your_api_key_here
```

The API key should never be committed to GitHub.

### 5. Run the FastAPI backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

### 6. Open the FastAPI documentation

Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The `/api/agent` endpoint can be tested directly through the Swagger interface.

---

## Docker

The backend also includes a Dockerfile for containerised deployment.

The project can be built and run using Docker according to the provided Docker configuration.

The Gemini API key should be supplied as an environment variable when running the container rather than being included in the Docker image.

---

## Design Decisions

### LangChain Agent

LangChain was introduced for Assessment 3 to provide an agent architecture capable of selecting and using tools instead of relying only on direct LLM responses.

### Google Gemini

Google Gemini is used as the language model because it provides the language-generation capability required by the StudyMate application.

### Tool-based study planning

The study-planning function was implemented as a LangChain tool so that the agent can determine when a structured study-planning action is useful.

### Internal state

An explicit state structure was introduced to track the user's message, conversation history, response, tool usage and execution status.

### FastAPI

FastAPI provides REST API endpoints between the frontend and AI backend and automatically provides interactive API documentation through Swagger.

### pytest

pytest was selected to provide automated testing of the state management, tool behaviour, agent execution and API endpoints.

### Environment variables

The Gemini API key is stored using environment variables to prevent credentials from being exposed in source code.

---

## Reuse of Assessment 2 Foundation

The Assessment 3 project builds upon the StudyMate AI application developed for Assessment 2.

The original foundation provided:

* FastAPI backend
* HTML/CSS/JavaScript frontend
* Google Gemini integration
* Conversation history
* Input validation
* Message sanitisation
* Docker configuration

For Assessment 3, the application was extended with new single-agent functionality rather than simply reusing the original chatbot unchanged.

The Assessment 3 additions include:

* LangChain agent
* Agent state management
* Tool calling
* Study-planning tool
* `/api/agent` endpoint
* Logging
* Additional guardrails
* Automated pytest testing
* Agent failure handling

---

## Limitations

The current system has several limitations:

* Agent state is maintained in memory and is not persistent across application restarts.
* The study-planning tool provides a simple rule-based study plan rather than a fully personalised timetable.
* The application depends on access to the Google Gemini API.
* The current system does not use a persistent database for conversation state.
* LLM responses may vary between requests.

---

## Future Improvements

Potential future improvements include:

* Persistent user accounts and conversation storage
* Database-backed agent state
* More study-planning tools
* Personalised study schedules
* Additional academic assistance tools
* Improved monitoring and logging
* More comprehensive mocked-agent testing
* Authentication and user-specific sessions

---

## GitHub Repository

The Assessment 3 repository is:

https://github.com/akrishtaale0224-wq/COIT12204_Assessment3

---

## AI Usage Statement

Generative AI was used during development to assist with understanding programming concepts, troubleshooting errors, improving code structure and working with technologies including FastAPI, LangChain, Google Gemini, Docker and pytest.

AI-generated suggestions were reviewed, adapted and tested during development. The final implementation was tested by the developer, including execution of the automated pytest suite and manual testing of the FastAPI agent endpoint.
