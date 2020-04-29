from typing import *
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import Member, User, Note, Board
from rest.schemas import NoteBase
from .permissions.services import Validator


def validate_note_creation(board_id: int, user: User, db: Session) -> Member:
    board = db.query(Board).get(board_id)
    # Mb refactor to another 404 way
    if not board:
        raise HTTPException(status_code=404, detail="Board is not exists")
    # Validate member
    member = (
        db.query(Member)
        .filter(
            Member.user_id == user.id
            and Member.board_id == board_id
        )
        .first()
    )
    if not member or not Validator(member).is_writable():
        raise HTTPException(status_code=400, detail="You have not enough permissions.")
    return member, board


def create_note(item: NoteBase, board_id: int, user: User, db: Session):
    # Validate board and member data
    member, board = validate_note_creation(board_id, user, db)
    # Create note
    creation_data = item.dict()
    note = Note(
        member=member,
        board=board,
        **creation_data
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note
