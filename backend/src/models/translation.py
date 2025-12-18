from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class TranslationPair(Base):
    __tablename__ = "translation_pairs"

    id = Column(String, primary_key=True, index=True)
    chapter_id = Column(String, nullable=False)  # ID of the chapter this translation belongs to
    content_en_id = Column(String)  # ID of the English content source
    content_ur = Column(Text)  # Urdu translation of the content
    translation_quality = Column(String)  # draft, reviewed, published
    translator_id = Column(String)  # ID of the translator (AI or human)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())