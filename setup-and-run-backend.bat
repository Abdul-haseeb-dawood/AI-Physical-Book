@echo off
echo Setting up Python virtual environment and installing dependencies...
cd /d "C:\Users\hp\Desktop\book\ai-bases-book\backend"

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run the backend server
echo Starting RAG Chatbot backend server...
python -m uvicorn main:app --reload --port 8000