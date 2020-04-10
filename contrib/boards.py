from sqlalchemy.orm import Session
from rest.schemas import BoardCreate
from .permissions.services import Permissions
from models import Board, Member
from contextlib import contextmanager


@contextmanager
def transaction(db: Session):
    """Simple transaction implementation in context manager"""
    try:
        db.begin_nested()
        yield
    except Exception as e:
        db.rollback()
        raise e
    finally:
        pass


def create_board(db: Session, board_data: BoardCreate):
    validated_data = board_data.dict()
    user_id = validated_data.pop("user")
    with transaction(db):
        # Create board
        board = Board(**validated_data)
        db.add(board)
        db.commit()
        db.refresh(board)
        # Create board owner
        owner: Member = (
            Permissions(
                db,
                board_id=board.id,
                user_id=user_id
            )
            .create_owner()
        )
    return board
