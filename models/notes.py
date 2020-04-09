import sqlalchemy as models
from sqlalchemy.orm import relationship
from .base import Base
from .boards import Board
from .user import User


class Note(Base):
    __tablename__ = "notes"

    id = models.Column(
        models.Integer, primary_key=True,
        index=True, unique=True
    )
    note = models.Column(models.String)
    user = models.Column(
        models.Integer, models.ForeignKey("users.id")
    )
    board = models.Column(
        models.Integer, models.ForeignKey("boards.id")
    )
    user_id = relationship(User)
    board_id = relationship(Board)
