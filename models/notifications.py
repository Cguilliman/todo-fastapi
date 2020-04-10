import sqlalchemy as models
from sqlalchemy.orm import relationship
from .base import Base
from .user import User


class Notification(Base):
    __tablename__ = "notifications"

    id = models.Column(
        models.Integer, primary_key=True,
        index=True, unique=True
    )
    title = models.Column(models.String)
    notification = models.Column(models.String)
    created_at = models.Column(models.DateTime)
    # Relations
    user_id = models.Column(
        models.Integer, models.ForeignKey("users.id")
    )
    user = relationship(User)
