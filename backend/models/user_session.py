from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserSession(BaseModel):
    """
    Represents a user's current interaction session with the chat system
    """
    session_id: UUID
    user_id: Optional[UUID] = None
    created_timestamp: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    active_status: bool = True

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"

    def __str__(self):
        return f"UserSession(id={self.session_id}, active={self.active_status})"