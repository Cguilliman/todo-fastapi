from typing import *

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import Note, get_db, User, Board, Member
from contrib.auth.auth import get_current_user
from contrib.notes import create_note
from shared.routers import delete_object
from ..schemas import NoteBase, NoteReceive


router = APIRouter()


@router.get("/{board_id}/list", response_model=List[NoteReceive])
def note_list(board_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(Note)
        .join(Board, Member)
        .filter(
            Board.id == board_id
            and Member.user_id == user.id
        )
        .all()
    )


@router.get("/{note_id}/receive", response_model=NoteReceive)
def note_receive(note_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(Note)
        .join(Board, Member)
        .filter(
            Note.id == note_id
            and Member.user_id == user.id
        )
        .first()
    )


@router.post("/{board_id}/create", response_model=NoteReceive)
def note_create(item: NoteBase, board_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_note(item, board_id, user, db)


@router.delete("/{note_id}/delete")
def note_delete(note_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = (
        db.query(Note)
        .join(Member)
        .filter(
            Member.user_id == user.id
            and Note.id == note_id
        )
        .first()
    )
    return delete_object(db, note)
