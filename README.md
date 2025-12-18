# Physical AI & Humanoid Robotics Book with RAG Chatbot

This project implements a Retrieval-Augmented Generation (RAG) chatbot that allows readers to ask questions about the book content and receive accurate answers based only on the book material. The chatbot appears as a floating button on the right side of all pages.

## Features

- **Floating Chat Widget**: A chat button appears on the right side of every page
- **Context-Aware Responses**: Answers consider the current chapter/section
- **Selected Text Queries**: Ask questions specifically about highlighted text
- **Secure & Reliable**: Rate limiting, input validation, and security measures
- **Fast Responses**: Caching layer for improved performance

## Tech Stack

- **Frontend**: Docusaurus with React components
- **Backend**: FastAPI
- **AI/ML**: OpenAI GPT models and embedding service
- **Vector Database**: Qdrant
- **Database**: Neon Postgres (optional, for chat history)

## Architecture

The system consists of:
1. An embedding pipeline that processes book markdown files
2. A vector database (Qdrant) storing the embedded content
3. A FastAPI backend handling queries and RAG processing
4. A React frontend component embedded in the Docusaurus site

## Installation and Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with your API keys:
   ```env
   GEMINI_API_KEY=AIzaSyB8LVwU_D6hq1rW5r7aSdC_9htU4LipJ00
   QDRANT_URL=https://2134dfd0-9e1d-4561-9378-a3b7eecdd74d.europe-west3-0.gcp.cloud.qdrant.io
   QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.jRMgTFfyIjn6d8v-ib5X2AF4MuwXYLI8m2ky75fLDaM
   QDRANT_COLLECTION_NAME=book_content
   EMBEDDING_MODEL=text-embedding-3-small
   GPT_MODEL=gpt-3.5-turbo
   RATE_LIMIT_REQUESTS=10
   RATE_LIMIT_WINDOW=60
   ```

5. Run the backend:
   ```bash
   python -m uvicorn main:app --reload --port 8000
   ```

### Frontend (Docusaurus) Setup

1. Navigate to the ai-book directory:
   ```bash
   cd ai-book
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run start
   ```

## Usage

1. The chat widget appears as a floating button on the bottom right of every page
2. Click to open the chat interface
3. Ask questions about the book content
4. The chatbot will respond with information from the book only

## API Endpoints

- `POST /api/chat`: General chat endpoint
- `POST /api/chat/selected-text`: Chat about selected text
- `GET /health`: Health check

## Security Measures

- Rate limiting to prevent abuse
- Input validation and sanitization
- Prompt injection protection
- Secure API key authentication (optional)

## Deployment

The backend can be deployed to any platform that supports Python/FastAPI. The frontend components integrate with the Docusaurus build process.