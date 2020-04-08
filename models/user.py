import sqlalchemy as models
from .base import Base


class User(Base):
    __tablename__ = "user"

    username = models.Column(models.String)
    email = models.Column(models.String)
    password = models.Column(models.String)
    is_active = models.Column(models.Boolean, default=False)
    is_admin = models.Column(models.Boolean, default=False)
