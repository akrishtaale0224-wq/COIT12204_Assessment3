# StudyMate AI

**COIT12204 – AI-Assisted Software Development**
**Assessment 2 – Web-Based LLM Chatbot Application**

StudyMate AI is a web-based university study assistant that allows students to ask academic and technical questions. It uses Google Gemini to generate responses.

## Technologies

* Frontend: HTML, CSS, JavaScript
* Backend: Python FastAPI
* LLM: Google Gemini API
* Deployment: Docker and Render
* Version Control: Git and GitHub

## Features

* Chat interface for students
* User and AI messages
* Typing/loading indicator
* Conversation history
* New Chat function
* Gemini AI responses
* Input validation and sanitisation
* FastAPI API endpoints
* Docker deployment

## Architecture

```text
Frontend
HTML / CSS / JavaScript
        ↓
FastAPI Backend
        ↓
Google Gemini API
```

The frontend sends messages to the FastAPI backend. The backend validates the input, manages conversation history and sends the conversation to Gemini. The response is then returned to the frontend.

## Main API Endpoints

### `/api/chat`

Accepts a user message and returns a Gemini-generated response.

### `/api/chat/new`

Clears the current conversation history and starts a new chat.

### `/api/health`

Checks whether the backend is running.

## Setup

Clone the repository:

```bash
git clone https://github.com/akrishtaale0224-wq/COIT12204-StudyMate-AI.git
cd COIT12204-StudyMate-AI
```

Install the backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the backend folder:

```text
GEMINI_API_KEY=your_api_key_here
```

Run the FastAPI backend:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Design Decisions

FastAPI was selected because it provides a simple way to create REST APIs and automatically provides Swagger documentation.

Google Gemini was selected as the LLM provider for generating chatbot responses.

An in-memory Python list is used to maintain conversation history during the current session.

The Gemini API key is stored as an environment variable rather than in the frontend code.

Docker was used to containerise the backend, and Render was used for cloud deployment.

## Deployment

**Live Application:**

https://coit12204-studymate-ai-2.onrender.com

**GitHub Repository:**

https://github.com/akrishtaale0224-wq/COIT12204-StudyMate-AI

## AI Usage Statement

Generative AI was used during development to assist with understanding code, troubleshooting errors, improving code structure and working with Gemini, FastAPI, Docker and Render.

AI-generated suggestions were reviewed and tested before being used in the final application. The final implementation and testing were completed by the developer.
