import sqlalchemy as models
from sqlalchemy.orm import relationship
from .base import Base


class Board(Base):
    __tablename__ = "boards"

    id = models.Column(
        models.Integer, primary_key=True,
        index=True, unique=True
    )
    title = models.Column(models.String)
    members = relationship("Member", back_populates="board")
