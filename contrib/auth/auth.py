from typing import *
from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from models import get_db, User
from settings import SECRET_KEY, ALGORITHM
from .password import verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user(db, username)
    if not user or not verify_password(user.password, password):
        return
    return user


def create_access_token(user: User, expires_delta: timedelta = None):
    to_encode = create_payload(user)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    if current_user := get_current_user_or_anonymous(db, token):
        return current_user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user_or_anonymous(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Union[User, bool]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            return False
    except PyJWTError:
        return False
    user = get_user(db, username=username)
    if user is None:
        return False
    return user


def create_payload(user: User):
    return {
        "username": user.username,
        "password": user.password,
        # TODO: format to json encode
        # "last_login": user.last_login,
    }
