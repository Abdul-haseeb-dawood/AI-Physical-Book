from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    content_en = Column(Text)  # English content in Markdown format
    content_ur = Column(Text)  # Urdu content in Markdown format
    metadata = Column(Text)  # JSON string for additional chapter metadata
    previous_chapter_id = Column(String)  # ID of the previous chapter in the sequence
    next_chapter_id = Column(String)  # ID of the next chapter in the sequence
    section = Column(String)  # Section this chapter belongs to
    difficulty_level = Column(String)  # beginner, intermediate, advanced
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())