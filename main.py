from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from logging.handlers import RotatingFileHandler
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
APP_VERSION = "1.1.0"

# --- Logging Setup ---
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(
            "mcp_logs.txt",
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8"
        )
    ]
)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="MCP Server API",
    description="A FastAPI application for chat and other services.",
    version=APP_VERSION
)

router = APIRouter(prefix="/api/v1")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS != ["*"] else ["*"],  # For dev allow all
    allow_credentials=True,
    allow_methods=["*"],  # Enables POST, GET, OPTIONS, etc.
    allow_headers=["*"]
)

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    model: str
    message: str

# --- Routes ---
@app.get("/")
async def root():
    return {"message": f"Welcome to MCP Server API v{APP_VERSION}", "status": "running"}

@router.get("/health")
async def health_check():
    return {"status": "✅ MCP server is healthy", "version": APP_VERSION}

@router.post("/chat")
async def chat(chat_request: ChatRequest):
    try:
        # Replace this with your real AI model call (OpenRouter, etc.)
        reply = f"Echo from MCP Server: {chat_request.message}"
        return {"response": reply}
    except Exception as e:
        logging.error(f"Error processing chat request: {e}", exc_info=True)
        return PlainTextResponse(f"Internal Server Error: {str(e)}", status_code=500)

@router.get("/logs", response_class=PlainTextResponse)
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

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    platform = "Render" if os.getenv("RENDER") == "true" else "Local"
    logging.info(f"✅ MCP Server v{APP_VERSION} started on {platform}")
    logging.info(f"Allowed Origins: {ALLOWED_ORIGINS}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
