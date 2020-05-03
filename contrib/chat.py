from typing import *

from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import Member, Board, Message, User
from ws.schemas import MessageSchema


def create_message(board_id: int, user: User, data: MessageSchema, db: Session) -> (Message, Board, Member):
    # Validate board
    board = db.query(Board).get(board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board is not exists.")
    # Validate member
    member = (
        db.query(Member)
        .filter(
            Member.user_id == user.id
            and Member.board_id == board.id
        )
        .first()
    )
    if not member:
        raise HTTPException(status_code=404, detail="Unknown")
    # Create message
    message = Message(
        board_id=board_id,
        message=data.message,
        member=member.id,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message, board, member


def build_chat_message(message: Message, board: Board = None, member: Member = None):
    if not board:
        board = message.board
    if not member:
        member = message.member

    return {
        "board_id": board.id,
        "board_title": board.title,
        "message": message.message,
        "member": {
            "id": member.id,
            "username": member.user.username,
            "user_id": member.user.id,
        },
    }
