from enum import Enum
import sqlalchemy as models
from sqlalchemy.orm import relationship

from .base import Base
from contrib.permissions.consts import MemberPermissions


class Member(Base):
    __tablename__ = "members"

    id = models.Column(
        models.Integer, primary_key=True, unique=True, index=True
    )
    permissions = models.Column(
        models.Enum(MemberPermissions)
    )
    # Relations
    board_id = models.Column(
        models.Integer, models.ForeignKey("boards.id")
    )
    user_id = models.Column(
        models.Integer, models.ForeignKey("users.id")
    )
    board = relationship("Board", back_populates="members")
    user = relationship("User", back_populates="members")
