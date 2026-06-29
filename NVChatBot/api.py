from pathlib import Path
import os

from dotenv import load_dotenv

# ---------------------------------------------------
# Load .env BEFORE importing the agent
# ---------------------------------------------------
env_path = Path(__file__).parent / ".env"
loaded = load_dotenv(dotenv_path=env_path)

print("=" * 60)
print("ENV FILE FOUND :", loaded)
print("ENV PATH       :", env_path)
print("GOOGLE_API_KEY :", os.getenv("GOOGLE_API_KEY"))
print("=" * 60)

from fastapi import FastAPI
from pydantic import BaseModel

from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService

from NVChatBot.agent import root_agent

# ---------------------------------------------------
# FastAPI App
# ---------------------------------------------------
app = FastAPI(title="NexVitals AI API")


# ---------------------------------------------------
# Request DTO
# ---------------------------------------------------
class ChatRequest(BaseModel):
    message: str


# ---------------------------------------------------
# ADK Session Service
# ---------------------------------------------------
session_service = InMemorySessionService()


# ---------------------------------------------------
# ADK Runner
# ---------------------------------------------------
runner = Runner(
    app_name="NVChatBot",
    agent=root_agent,
    session_service=session_service,
    auto_create_session=True
)


# ---------------------------------------------------
# Health Check
# ---------------------------------------------------
@app.get("/")
def home():
    return {
        "status": "NexVitals AI API Running"
    }


# ---------------------------------------------------
# Chat Endpoint
# ---------------------------------------------------
@app.post("/chat")
async def chat(request: ChatRequest):

    response_text = ""

    async for event in runner.run_async(
        user_id="web-user",
        session_id="default-session",
        new_message=types.UserContent(
            parts=[
                types.Part(text=request.message)
            ]
        )
    ):

        if event.content and event.content.parts:

            for part in event.content.parts:

                if getattr(part, "text", None):
                    response_text += part.text

    return {
        "reply": response_text
    }