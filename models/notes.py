import sqlalchemy as models
from sqlalchemy.orm import relationship
from .base import Base
from .boards import Board
from .members import Member


class Note(Base):
    __tablename__ = "notes"

    id = models.Column(
        models.Integer, primary_key=True,
        index=True, unique=True
    )
    note = models.Column(models.String)
    # Relations
    board_id = models.Column(
        models.Integer, models.ForeignKey("boards.id")
    )
    member_id = models.Column(
        models.Integer, models.ForeignKey("members.id")
    )
    board = relationship(Board)
    member = relationship(Member)
