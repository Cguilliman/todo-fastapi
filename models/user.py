import datetime
import sqlalchemy as models
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = models.Column(
        models.Integer, primary_key=True,
        index=True, unique=True
    )
    username = models.Column(models.String)
    email = models.Column(models.String)
    password = models.Column(models.String)
    is_active = models.Column(models.Boolean, default=False)
    is_admin = models.Column(models.Boolean, default=False)
    last_login = models.Column(models.DateTime, default=datetime.datetime.utcnow)
    members = relationship("Member")
