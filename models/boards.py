import sqlalchemy as models
from sqlalchemy.orm import relationship
from .base import Base
from .user import User


class Board(Base):
    __tablename__ = "board"

    title = models.Column(models.String)
    user = models.Column(
        models.Integer, models.ForeignKey("user.id")
    )
    user_id = relationship(User)
