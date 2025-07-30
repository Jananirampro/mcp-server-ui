@echo off
echo 🟢 Activating virtual environment...
call venv\Scripts\activate.bat

echo 🧪 Checking Python version...
python --version

echo 📦 Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo 🚀 Starting MCP Server...
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause