from typing import *

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import Board, get_db, User, Member
from contrib.boards import create_board, add_member
from .schemas import (
    BoardReceive, BoardCreate,
    UserReceive, UserCreate,
    MemberAdd, MemberAddReceive
)


router = APIRouter()


@router.get("/board/list", response_model=List[BoardReceive])
def board_list(db: Session = Depends(get_db)):
    return db.query(Board).all()


@router.post("/board/create", response_model=BoardReceive)
def board_create(item: BoardCreate, db: Session = Depends(get_db)):
    return create_board(db, item)


@router.post("/board/member/add", response_model=MemberAddReceive)
def board_member_add(item: MemberAdd, db: Session = Depends(get_db)):
    return add_member(db, item)


@router.delete("/board/member/{member_id}/delete")
def board_member_delete(member_id: int, db: Session = Depends(get_db)):
    db.query(Member).filter(Member.id == member_id).delete()
    return {"Status": "OK"}


@router.post("/user/create")
def user_create(item: UserCreate, db: Session = Depends(get_db)):
    validated_data = item.dict()
    validated_data["is_active"] = True
    user = User(**validated_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
