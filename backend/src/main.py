from fastapi import FastAPI
from src.api import auth_routes
from src.api import chapter_routes
from src.api import chat_routes
from src.api import personalization_routes
from src.api import translation_routes
from src.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI & Robotics Book Platform API", version="1.0.0")

# Include API routes
app.include_router(auth_routes.router)
app.include_router(chapter_routes.router)
app.include_router(chat_routes.router)
app.include_router(personalization_routes.router)
app.include_router(translation_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI & Robotics Book Platform API"}