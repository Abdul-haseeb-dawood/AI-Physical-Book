@echo off
echo Starting RAG Chatbot backend server...
cd /d "C:\Users\hp\Desktop\book\ai-bases-book\backend"
python -m uvicorn main:app --reload --port 8000