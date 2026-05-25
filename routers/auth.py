from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt

from db_config.db import get_db, User
from schemas.schemas import UserCreate, UserResponse, Token
from utils.hashing import hash_password, verify_password
from utils.jwt_token import create_jwt_token
from core.dependencies import get_current_user

router = APIRouter(tags=["Authentication"])

@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    is_first_user = db.query(User).count() == 0
    assigned_role = "admin" if is_first_user else "user"

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=assigned_role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password( user.hashed_password, form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    token_payload = {"sub": user.email, "id": user.id, "role": user.role}
    access_token = create_jwt_token(data=token_payload)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == current_user["id"]).first()
    return db_user
