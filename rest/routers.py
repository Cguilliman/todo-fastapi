from typing import *

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import Board, get_db, User
from contrib.boards import create_board
from .schemas import BoardReceive, BoardCreate, UserReceive, UserCreate


router = APIRouter()


@router.get("/boards/list", response_model=List[BoardReceive])
def boards_list(db: Session = Depends(get_db)):
    # print(db.query(Board).all()[-1].members[0].permissions)
    return db.query(Board).all()


@router.post("/boards/create", response_model=BoardReceive)
def boards_create(item: BoardCreate, db: Session = Depends(get_db)):
    return create_board(db, item)


@router.post("/user/create")
def user_create(item: UserCreate, db: Session = Depends(get_db)):
    validated_data = item.dict()
    validated_data["is_active"] = True
    user = User(**validated_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
