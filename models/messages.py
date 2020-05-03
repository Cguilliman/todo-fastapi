import sqlalchemy as models
from sqlalchemy.orm import relationship

from .base import Base
from .members import Member
from .boards import Board


class Message(Base):
    __tablename__ = "messages"

    id = models.Column(
        models.Integer, primary_key=True, unique=True, index=True
    )
    message = models.Column(models.String)
    created_at = models.Column(models.DateTime)
    # Relationship
    member_id = models.Column(
        models.Integer, models.ForeignKey("members.id")
    )
    board_id = models.Column(
        models.Integer, models.ForeignKey("boards.id")
    )
    member = relationship(Member)
    board = relationship(Board)
