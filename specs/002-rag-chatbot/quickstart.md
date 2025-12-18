# Quickstart Guide: RAG Chatbot Development

## Prerequisites

- Python 3.11+
- Node.js 18+ (for Docusaurus)
- Docker (for local Qdrant instance)
- OpenAI API key
- Qdrant API key (or local instance)

## Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-bases-book
   ```

2. Set up backend environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create environment file:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## Configuration

1. Set up environment variables in `.env`:
   ```
   GEMINI_API_KEY=AIzaSyB8LVwU_D6hq1rW5r7aSdC_9htU4LipJ00
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   DATABASE_URL=your_database_url
   SECRET_KEY=your_secret_key
   RATE_LIMIT_REQUESTS=10
   RATE_LIMIT_WINDOW=60  # seconds
   ```

## Running the Application

1. Start Qdrant (if using local instance):
   ```bash
   docker run -d --name qdrant-container -p 6333:6333 qdrant/qdrant
   ```

2. Start the backend:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

3. In a new terminal, start the frontend (Docusaurus):
   ```bash
   cd ai-book
   npm install
   npm run start
   ```

## Development Workflow

1. Run the backend tests:
   ```bash
   cd backend
   pytest
   ```

2. Run the backend in development mode (auto-reloads on code changes):
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

3. Add new book content to be indexed by adding markdown files to the docs directory and running the embedding pipeline.

## API Endpoints

- `POST /chat`: General chat endpoint
- `POST /chat/selected-text`: Chat about selected text
- `GET /health`: Health check endpoint

## Frontend Integration

The chatbot widget is integrated into the Docusaurus site as a custom plugin. To modify the widget appearance or behavior:

1. Look in `ai-book/src/components/ChatWidget` for the React component
2. The widget state is managed via React Context and communicates with the backend via API calls
3. Text selection functionality is implemented using the browser's Selection API