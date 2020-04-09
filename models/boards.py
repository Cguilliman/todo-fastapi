import sqlalchemy as models
from sqlalchemy.orm import relationship, Session
from .base import Base
from .user import User


class Board(Base):
    __tablename__ = "boards"

    id = models.Column(
        models.Integer, primary_key=True,
        index=True, unique=True
    )
    title = models.Column(models.String)
    user = models.Column(
        models.Integer, models.ForeignKey("users.id")
    )
    user_id = relationship(User)
