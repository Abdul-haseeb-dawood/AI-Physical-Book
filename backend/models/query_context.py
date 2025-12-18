from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class QueryContext(BaseModel):
    """
    Represents the context in which a query is made (page, chapter, selected text)
    """
    query_context_id: Optional[UUID] = None
    session_id: UUID
    current_page: Optional[str] = None
    current_chapter: Optional[str] = None
    selected_text: Optional[str] = None
    query_timestamp: Optional[datetime] = None
    context_metadata: Optional[dict] = None

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"

    def __str__(self):
        return f"QueryContext(id={self.query_context_id}, chapter={self.current_chapter})"