from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChapterBase(BaseModel):
    title: str
    slug: str
    content_en: Optional[str] = None
    content_ur: Optional[str] = None
    metadata: Optional[str] = None  # JSON string
    previous_chapter_id: Optional[str] = None
    next_chapter_id: Optional[str] = None
    section: Optional[str] = None
    difficulty_level: Optional[str] = None

class ChapterCreate(ChapterBase):
    title: str
    slug: str
    content_en: str

class ChapterResponse(ChapterBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True