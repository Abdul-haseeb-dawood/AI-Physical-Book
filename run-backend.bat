@echo off
echo Starting RAG Chatbot backend server...
cd /d "C:\Users\hp\Desktop\book\ai-bases-book\backend"

REM Activate virtual environment
call venv\Scripts\activate

REM If virtual environment doesn't exist, create it
if errorlevel 1 (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Run the backend server
echo Starting backend server...
python -m uvicorn main:app --reload --port 8000