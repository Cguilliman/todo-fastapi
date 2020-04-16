from typing import *

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Board, get_db, Member, User
from contrib.boards import create_board, add_member
from contrib.permissions.services import Validator
from contrib.auth.auth import get_current_user
from shared.routers import delete_object
from ..schemas import (
    BoardReceive, BoardCreate,
    MemberAdd, MemberAddReceive,
)

router = APIRouter()


@router.get("/list", response_model=List[BoardReceive])
def board_list(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(Board)
        .join(Member)
        .filter(Member.user_id == user.id)
        .all()
    )


@router.post("/create", response_model=BoardReceive)
def board_create(item: BoardCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_board(db, item, user)


@router.post("/member/add", response_model=MemberAddReceive)
def board_member_add(item: MemberAdd, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return add_member(db, item, user)


@router.delete("/{board_id}/delete")
def board_delete(board_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    board_obj = (
        db.query(Board)
        .join(Member)
        .filter(
            Board.id == board_id
            and Member.user_id == user.id
        )
        .first()
    )
    return delete_object(db, board_obj)


@router.delete("/member/{member_id}/delete")
def board_member_delete(member_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    member_obj = db.query(Member).get(member_id)
    # Check is member exists
    if not member_obj:
        raise HTTPException(status_code=400, detail="Object is not found")
    # Get current user member
    current_member = (
        db.query(Member)
        .filter(
            Member.board_id == member_obj.board_id
            and Member.user_id == user.id
        )
        .first()
    )
    # Check is current member have enough permissions
    if not current_member or not Validator(current_member).is_editable():
        raise HTTPException(
            status_code=400,
            detail="You have not enough permissions to edit board members."
        )
    # Delete object
    return delete_object(db, member_obj)
