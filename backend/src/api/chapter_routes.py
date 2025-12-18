from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.models.chapter import Chapter
from src.schemas.chapter import ChapterResponse

router = APIRouter(prefix="/api/chapters", tags=["chapters"])

@router.get("/", response_model=List[ChapterResponse])
async def get_all_chapters(db: Session = Depends(get_db)):
    chapters = db.query(Chapter).all()
    return chapters

@router.get("/{slug}", response_model=ChapterResponse)
async def get_chapter_by_slug(slug: str, db: Session = Depends(get_db)):
    chapter = db.query(Chapter).filter(Chapter.slug == slug).first()
    if not chapter:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter