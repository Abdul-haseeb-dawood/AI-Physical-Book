from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)  # Nullable for anonymous sessions
    chapter_id = Column(String, nullable=True)  # Optional: context for the session
    selected_text = Column(Text)  # Text selected by the user for focused Q&A
    query_history = Column(Text)  # JSON string representing the query history
    mode = Column(String, nullable=False)  # Options: general, chapter-specific, selected-text-only
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())