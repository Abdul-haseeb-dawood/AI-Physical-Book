from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from src.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserResponse
from src.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["authentication"])

auth_service = AuthService()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = auth_service.get_password_hash(user_data.password)
    
    # Create user
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        skill_level=user_data.skill_level,
        software_background=user_data.software_background,
        hardware_experience=user_data.hardware_experience
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(
        id=db_user.id,
        email=db_user.email,
        skill_level=db_user.skill_level,
        created_at=db_user.created_at
    )

@router.post("/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": user}