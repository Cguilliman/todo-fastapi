from typing import *

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import Board, get_db, User
from .schemas import BoardReceive, BoardCreate, UserReceive, UserCreate


router = APIRouter()


@router.get("/boards/list", response_model=List[BoardReceive])
def boards_list(db: Session = Depends(get_db)):
    return db.query(Board).all()


@router.post("/boards/create")
def boards_create(item: BoardCreate, db: Session = Depends(get_db)):
    board = Board(**item.dict())
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


@router.post("/user/create")
def user_create(item: UserCreate, db: Session = Depends(get_db)):
    validated_data = item.dict()
    validated_data["is_active"] = True
    user = User(**validated_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
