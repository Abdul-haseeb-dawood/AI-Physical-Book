from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class ChatMessage(BaseModel):
    """
    Represents a single exchange between user and system in the chat
    """
    id: Optional[UUID] = None
    session_id: UUID
    user_id: Optional[UUID] = None
    query_text: str
    response_text: str
    timestamp: Optional[datetime] = None
    source_context: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = None

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"

    def __str__(self):
        return f"ChatMessage(id={self.id}, session_id={self.session_id})"