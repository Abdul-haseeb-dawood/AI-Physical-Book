from sqlalchemy import Column, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class PersonalizationProfile(Base):
    __tablename__ = "personalization_profiles"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    chapter_id = Column(String, ForeignKey("chapters.id"), nullable=False)  # Assumes a chapters table exists
    personalized_summary = Column(Text)
    recommended_prerequisites = Column(Text)  # JSON string representing array of chapter IDs
    complexity_adjustment = Column(Float, default=1.0)  # Between 0.5 and 2.0
    content_modifications = Column(Text)  # JSON string for specific modifications
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())