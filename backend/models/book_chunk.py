from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class BookChunk(BaseModel):
    """
    Represents a chunk of book content with metadata for RAG system
    """
    content_id: str
    chapter: str
    section: str
    page: Optional[str] = None
    content_text: str
    embedding_vector: List[float]
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None

    class Config:
        # Allow extra fields for flexibility with metadata
        extra = "allow"

    def __str__(self):
        return f"BookChunk(id={self.content_id}, chapter={self.chapter}, section={self.section})"