from typing import *

from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import User
from rest.schemas import SchemaRegistration
from .password import hash_password


def validate_user_data(data: SchemaRegistration, db: Session) -> SchemaRegistration:
    if bool(db.query(User).filter(User.username == data.username).first()):
        raise HTTPException(status_code=400, detail="Same username already exists.")
    return data


def create_user(data: SchemaRegistration, db: Session):
    validated_data: SchemaRegistration = validate_user_data(data, db)
    user = User(
        username=validated_data.username,
        password=hash_password(validated_data.password1)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(user)
    return User
