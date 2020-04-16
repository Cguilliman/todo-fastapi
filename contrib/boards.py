from typing import *
from fastapi import HTTPException
from sqlalchemy.orm import Session

from rest.schemas import BoardCreate, MemberAdd
from .permissions.services import Permissions, Validator
from models import Board, Member, User
from shared.transactions import atomic


def create_board(db: Session, board_data: BoardCreate, user: User):
    validated_data = board_data.dict()
    with atomic(db):
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
                user_id=user.id
            )
            .create_owner()
        )
    return board


def add_member(db: Session, adding_dto: MemberAdd, user: User) -> Member:
    # Validate schema data by database instance
    validated_data, member = validate_add_member(db, adding_dto, user)
    # Check is members existing
    if member:
        # Update member permissions
        member.permissions = validated_data.get("permissions")
    else:
        # Create new member by validated data
        member = Member(**validated_data)
        db.add(member)
    db.commit()
    db.refresh(member)
    return member


def validate_add_member(db: Session, dto: MemberAdd, user: User) -> (Dict, Board, Optional[Member]):
    # Get user and check is user with current id exists
    user = db.query(User).get(dto.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="User is not exists.")

    # TODO: Re-factor board-member getter to one query
    # Get board and check is board with current id exists
    board = db.query(Board).get(dto.board_id)
    if not board:
        raise HTTPException(status_code=400, detail="Board is not exists.")

    # Get current board member and check is authorized user has enough permissions
    current_member = (
        db.query(Member)
        .filter(
            Member.board_id == dto.board_id
            and Member.user_id == user.id
        )
    )
    if not current_member or not Validator(current_member).is_editable():
        raise HTTPException(
            status_code=400,
            detail="You has not enough permissions to edit current board`s members list."
        )

    # Get members with current id
    members = (
        db.query(Member)
        .filter(
            Member.board_id == dto.board_id
            and Member.user_id == dto.user_id
        )
        .all()
    )
    member = None
    if members:
        if len(members) > 1:
            # Normalize board members related to similar user
            member = normalize_board_member(members, db)[0]
        else:
            member = members[0]
    return dto.dict(), member


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
