from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY not found in .env")

# FastAPI app
app = FastAPI(title="MCP Server")

# ✅ Enable CORS for UI (allow all origins or restrict as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["https://your-ui-domain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request body model
class ChatRequest(BaseModel):
    message: str
    model: str = "mistralai/mistral-7b-instruct:free"  # Default model

# ✅ POST /chat endpoint
@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": req.model,
            "messages": [{"role": "user", "content": req.message}],
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        # Extract AI response text
        reply = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "Sorry, I couldn’t generate a response.")
        )

        return {"response": reply}

    except Exception as e:
        return {"error": f"Server error: {str(e)}"}
