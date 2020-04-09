from pydantic import BaseModel
from datetime import datetime
from models import Board


class BoardBase(BaseModel):
    title: str

    class Config:
        orm_mode = True


class BoardReceive(BoardBase):
    id: int


class BoardCreate(BoardBase):
    user: int


class UserBase(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class UserReceive(UserBase):
    id: int


class UserCreate(UserBase):
    password: str
