# utils/router_client.py

import os
import httpx
from dotenv import load_dotenv
import logging 

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print(f"🔑 API Key Loaded")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

async def call_model(model: str, message: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",  # Optional but good practice
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                OPENROUTER_BASE_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

    except httpx.HTTPStatusError as e:
        return f"❌ Error from model: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"
