from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.config import get_db
from app.utils.jwt_handler import create_access_token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return AuthService.register_user(db, user)

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
