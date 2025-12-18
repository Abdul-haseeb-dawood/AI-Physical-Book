"""
Database migration script for AI & Robotics Book Platform
"""
from sqlalchemy import create_engine, text
from src.database import DATABASE_URL
from src.models.user import Base as UserBase
from src.models.chat_session import Base as ChatSessionBase
from src.models.personalization import Base as PersonalizationBase
from src.models.chapter import Base as ChapterBase
from src.models.translation import Base as TranslationBase

def run_migrations():
    engine = create_engine(DATABASE_URL)
    
    # Create all tables
    UserBase.metadata.create_all(bind=engine)
    ChatSessionBase.metadata.create_all(bind=engine)
    PersonalizationBase.metadata.create_all(bind=engine)
    ChapterBase.metadata.create_all(bind=engine)
    TranslationBase.metadata.create_all(bind=engine)
    
    print("Database tables created successfully!")

if __name__ == "__main__":
    run_migrations()