from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# ✅ Allow all origins for now (can restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["https://your-ui-domain.com"] in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow POST, GET, etc.
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "MCP Server is running"}

@app.post("/chat")
async def chat_endpoint(request: dict):
    message = request.get("message", "")
    # Call OpenRouter API
    return {"response": f"Echo from MCP Server: {message}"}

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import os
from pydantic import BaseModel
from utils.router_client import call_model
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    filename="mcp_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"  # ✅ Prevent UnicodeDecodeError on Render
)

app = FastAPI()

class ChatRequest(BaseModel):
    model: str
    message: str

# ✅ Health check route
@app.get("/health")
async def health_check():
    return {"status": "✅ MCP server is healthy"}

# ✅ Main chat handler
@app.post("/chat")
async def chat(chat_request: ChatRequest):
    logging.info(f"Request received: {chat_request.model} | {chat_request.message}")
    try:
        print("👉 call_model type:", type(call_model))
        reply =  await call_model(chat_request.model, chat_request.message)
        logging.info(f"Response: {reply}")
        return {"response": reply}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"error": str(e)}

# ✅ View logs route
@app.get("/logs", response_class=PlainTextResponse)
async def get_logs():
    log_path = "mcp_logs.txt"
    if not os.path.exists(log_path):
        return "🚫 No logs available."

    try:
        with open(log_path, "r", encoding="utf-8") as log_file:
            content = log_file.read()
            return content if content else "📭 Log file is empty."
    except Exception as e:
        return f"❌ Error reading logs: {str(e)}"

# ✅ Print startup message for both Render and Local
@app.on_event("startup")
async def startup_event():
    platform = "Render" if os.environ.get("RENDER") == "true" else "Local"
    print(f"✅ MCP Server is running on {platform}")
    logging.info(f"✅ MCP Server started on {platform}")

# ✅ Local manual run block (Render ignores this)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render sets PORT; fallback to 10000
    print(f"🔧 Starting MCP server locally on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port)    
