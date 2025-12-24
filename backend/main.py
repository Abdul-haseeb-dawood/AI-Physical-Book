from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat_routes import router as chat_router
from config.settings import settings
import uvicorn


def create_app():
    app = FastAPI(
        title="RAG Chatbot API",
        description="API for the RAG chatbot system that answers questions based on book content",
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify your frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(chat_router)

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app

app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )