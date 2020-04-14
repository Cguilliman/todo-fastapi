from typing import *

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models import Board, get_db, User, Member
from contrib.boards import create_board, add_member
from .schemas import (
    BoardReceive, BoardCreate,
    UserReceive, UserCreate,
    MemberAdd, MemberAddReceive
)


router = APIRouter()



from datetime import datetime, timedelta

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password
    # return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.password):
        return False
    return user


def create_access_token(*, data: Dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


class Schema(BaseModel):
    username: str
    password: str


@router.post("/token")
def login_for_access_token(form_data: Schema, db: Session = Depends(get_db)):
    user: User = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# NOTE: only for test
@router.get("/users")
async def users(db: Session = Depends(get_db)):
    return db.query(User).all()


# TODO: add to global utils module
def delete_object(db: Session, object_id: int, model: "models.base.Base"):
    _object = db.query(model).get(object_id)
    if not _object:
        raise HTTPException(status_code=404, detail="Object is not found")
    db.delete(_object)
    db.commit()
    return {"status": "OK"}


@router.get("/board/list", response_model=List[BoardReceive])
def board_list(db: Session = Depends(get_db)):
    return db.query(Board).all()


@router.post("/board/create", response_model=BoardReceive)
def board_create(item: BoardCreate, db: Session = Depends(get_db)):
    return create_board(db, item)


@router.post("/board/member/add", response_model=MemberAddReceive)
def board_member_add(item: MemberAdd, db: Session = Depends(get_db)):
    return add_member(db, item)


@router.delete("/board/{board_id}/delete")
def board_delete(board_id: int, db: Session = Depends(get_db)):
    return delete_object(db, board_id, Board)


@router.delete("/board/member/{member_id}/delete")
def board_member_delete(member_id: int, db: Session = Depends(get_db)):
    return delete_object(db, member_id, Member)


@router.post("/user/create")
def user_create(item: UserCreate, db: Session = Depends(get_db)):
    validated_data = item.dict()
    validated_data["is_active"] = True
    user = User(**validated_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
