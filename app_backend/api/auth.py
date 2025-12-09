from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app_backend.schemas import UserCreate
from app_backend.models import User
from app_backend.db import get_session
from app_backend.utils import hash_password, create_access_token, verify_password

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, session: Session = Depends(get_session)):
    q = select(User).where(User.email == user.email)
    res = session.exec(q).first()
    if res:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    token = create_access_token({"sub": db_user.email, "user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(user: UserCreate, session: Session = Depends(get_session)):
    q = select(User).where(User.email == user.email)
    db_user = session.exec(q).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email, "user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}
