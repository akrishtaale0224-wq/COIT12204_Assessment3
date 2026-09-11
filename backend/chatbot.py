from google import genai
from google.genai import types

from .config import GEMINI_API_KEY


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to the .env file."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


SYSTEM_INSTRUCTION = """
You are StudyMate AI, a helpful university study assistant.

Your purpose is to help university students understand academic
and technical concepts clearly.

Guidelines:
- Explain concepts using simple and clear language.
- Provide examples when useful.
- Help students learn rather than simply giving unexplained answers.
- Be respectful and professional.
- Keep answers clear and organised.
- If you are uncertain about information, say so.
- Do not claim to have accessed information that you cannot access.
- Only use the conversation history provided in the current request.
- Do not assume information from previous conversations.
"""


def generate_response(messages):

    contents = []

    for message in messages:

        role = message.get("role")
        content = message.get("content", "")

        if not content:
            continue

        if role == "user":

            contents.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part(text=content)
                    ]
                )
            )

        elif role == "assistant":

            contents.append(
                types.Content(
                    role="model",
                    parts=[
                        types.Part(text=content)
                    ]
                )
            )


    if not contents:
        raise ValueError("No conversation contents were provided.")


    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION
        )
    )


    if not response.text:
        raise ValueError("Gemini returned an empty response.")


    return response.text