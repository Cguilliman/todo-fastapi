import sqlalchemy as models
from sqlalchemy.orm import relationship
from .base import Base
from .user import User


class Notification(Base):
    __tablename__ = "notification"

    title = models.Column(
        models.String
    )
    notification = models.Column(
        models.String
    )
    user = models.Column(
        models.Integer, models.ForeignKey("user.id")
    )
    user_id = relationship(User)
