from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings


# Create database engine
if settings.DATABASE_URL:
    engine = create_engine(settings.DATABASE_URL)
else:
    # Use a default SQLite database if no URL is provided
    engine = create_engine("sqlite:///./rag_chatbot.db")
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()