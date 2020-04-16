from typing import *
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import get_db, User
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from contrib.auth.auth import authenticate_user, create_access_token, get_current_user
from contrib.auth.registration import create_user
from ..schemas import (
    UserReceive, SchemaLogin, SchemaRegistration
)


router = APIRouter()


@router.post("/login")
def login_for_access_token(form_data: SchemaLogin, db: Session = Depends(get_db)):
    user: Optional[User] = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user=user, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserReceive)
async def user_receive(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/user/register/", response_model=UserReceive)
async def register(data: SchemaRegistration, db: Session = Depends(get_db)):
    return create_user(data, db)


# NOTE: only for test
@router.get("/users")
async def users(db: Session = Depends(get_db)):
    return db.query(User).all()
