from typing import *
from fastapi import HTTPException
from sqlalchemy.orm import Session
from contextlib import contextmanager

from rest.schemas import BoardCreate, MemberAdd
from .permissions.services import Permissions
from models import Board, Member, User


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


def add_member(db: Session, adding_dto: MemberAdd) -> Member:
    # Validate schema data by database instance
    validated_data, members = validate_add_member(db, adding_dto)
    # Check is members existing
    if members:
        if len(members) > 1:
            # Normalize board members related to similar user
            member = normalize_board_member(members, db)[0]
        else:
            member = members[0]
        # Update member permissions
        member.permissions = validated_data.get("permissions")
    else:
        # Create new member by validated data
        member = Member(**validated_data)
        db.add(member)
    db.commit()
    db.refresh(member)
    return member


def validate_add_member(db: Session, dto: MemberAdd) -> (Dict, Board, Optional[List[Member]]):
    data = dto.dict()
    # Get user and check is user with current id exists
    user = db.query(User).get(data.get("user_id"))
    if not user:
        raise HTTPException(status_code=400, detail="User is not exists.")

    # Get board and check is board with current id exists
    board = db.query(Board).get(data.get("board_id"))
    if not board:
        raise HTTPException(status_code=400, detail="Board is not exists.")

    # Get members with current id
    members = (
        db.query(Member)
        .filter(
            Member.board_id == data.get("board_id")
            and Member.user_id == data.get("user_id")
        )
        .all()
    )
    return data, members


def normalize_board_member(members: List[Member], db: Session) -> List[Member]:
    """Remove remove duplicated members"""
    normal_members: Dict[int, Member] = {}
    removing_members: List[int] = []

    for member in members:
        if member.user_id not in normal_members:
            normal_members[member.user_id] = member
        elif normal_members[member.user_id].permissions < member.permissions:
            removing_members.append(normal_members[member.user_id].id)
            normal_members[member.user_id] = member
        else:
            removing_members.append(member.id)
    # Remove db query
    db.query(Member).filter(Member.id in removing_members).delete()
    return list(normal_members.values())
