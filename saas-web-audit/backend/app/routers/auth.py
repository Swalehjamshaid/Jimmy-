
# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import User, Organization
from ..security import hash_password, verify_password, create_token
from ..schemas import RegisterRequest, LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(req: RegisterRequest):
    db: Session = SessionLocal()
    try:
        org = Organization(name=req.organization_name)
        db.add(org)
        db.flush()
        user = User(email=req.email, password_hash=hash_password(req.password), is_verified=True, role="Admin", organization_id=org.id)
        db.add(user)
        db.commit()
        return Token(access_token=create_token(user.id, "access"), refresh_token=create_token(user.id, "refresh"))
    finally:
        db.close()

@router.post("/login", response_model=Token)
def login(req: LoginRequest):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == req.email).first()
        if not user or not verify_password(req.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return Token(access_token=create_token(user.id, "access"), refresh_token=create_token(user.id, "refresh"))
    finally:
        db.close()
