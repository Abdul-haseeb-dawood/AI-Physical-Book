from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import logging

from models.query_context import QueryContext
from services.chat_service import ChatService
from middleware.rate_limit import rate_limit_middleware
from config.settings import settings


router = APIRouter(tags=["chat"])

# Request models
class ChatRequest(BaseModel):
    query: str
    page: Optional[str] = None
    chapter: Optional[str] = None
    selected_text: Optional[str] = None


class SelectedTextRequest(BaseModel):
    query: str
    selected_text: str
    page: Optional[str] = None
    chapter: Optional[str] = None


# Response models
class Source(BaseModel):
    content_id: str
    chapter: str
    section: str


class ChatResponse(BaseModel):
    response: str
    sources: List[Source]
    confidence: float


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: Request,
    chat_request: ChatRequest,
    _ = Depends(rate_limit_middleware)
):
    """
    General chat endpoint to receive queries and return responses based on book content
    """
    # Validate query length
    if len(chat_request.query) > 2000:
        raise HTTPException(status_code=400, detail="Query too long")

    # Create query context
    query_context = QueryContext(
        session_id=uuid.uuid4(),  # In real implementation, you'd retrieve this from session
        current_page=chat_request.page,
        current_chapter=chat_request.chapter,
        selected_text=chat_request.selected_text,
        context_metadata={"request_ip": request.client.host}
    )

    try:
        # Initialize chat service
        chat_service = ChatService()

        # Process the query
        result = chat_service.process_query(
            query=chat_request.query,
            query_context=query_context,
            ip_address=request.client.host
        )

        # Format response
        response = ChatResponse(
            response=result.get("response", "I couldn't find relevant information in the book to answer your question."),
            sources=[
                Source(
                    content_id=source.get("content_id", ""),
                    chapter=source.get("chapter", "Unknown"),
                    section=source.get("section", "Unknown")
                )
                for source in result.get("sources", [])
            ],
            confidence=result.get("confidence", 0.0)
        )

        return response
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/chat/selected-text", response_model=ChatResponse)
async def chat_selected_text_endpoint(
    request: Request,
    selected_text_request: SelectedTextRequest,
    _ = Depends(rate_limit_middleware)
):
    """
    Chat endpoint specifically for queries about selected text
    """
    # Validate query length
    if len(selected_text_request.query) > 2000 or len(selected_text_request.selected_text) > 2000:
        raise HTTPException(status_code=400, detail="Query or selected text too long")

    # Create query context
    query_context = QueryContext(
        session_id=uuid.uuid4(),  # In real implementation, you'd retrieve this from session
        current_page=selected_text_request.page,
        current_chapter=selected_text_request.chapter,
        selected_text=selected_text_request.selected_text,
        context_metadata={"request_ip": request.client.host}
    )

    try:
        # Initialize chat service
        chat_service = ChatService()

        # Process the query about selected text
        result = chat_service.process_query(
            query=selected_text_request.query,
            query_context=query_context,
            ip_address=request.client.host
        )

        # Format response
        response = ChatResponse(
            response=result.get("response", "I couldn't find relevant information in the book to answer your question about the selected text."),
            sources=[
                Source(
                    content_id=source.get("content_id", ""),
                    chapter=source.get("chapter", "Unknown"),
                    section=source.get("section", "Unknown")
                )
                for source in result.get("sources", [])
            ],
            confidence=result.get("confidence", 0.0)
        )

        return response
    except Exception as e:
        logging.error(f"Error in selected text chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")