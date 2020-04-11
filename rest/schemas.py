from typing import List
from pydantic import BaseModel, validator
from contrib.permissions.consts import MemberPermissions


class Editable(BaseModel):

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        """Dynamical add getter custom default field value by instance"""
        instance = super().from_orm(obj)
        # Get fields names from instance
        fields_names = instance.fields.keys()
        for field_name in fields_names:
            func_name = f"get_{field_name}"
            # Check valid function exists
            if (
                hasattr(instance, func_name)
                and (func := getattr(instance, func_name))
                and callable(func)
            ):
                setattr(instance, field_name, func())
        return instance


# Member schemas
class MemberBase(Editable):
    id: int
    user_id: int
    permissions: MemberPermissions

    def get_permissions(self):
        return MemberPermissions.get_label(self.permissions)


class MemberAdd(BaseModel):
    board_id: int
    permissions: MemberPermissions
    user_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            # Example
            'example': {
                "user_id": 1,
                "permissions": 2,
                "board_id": 1
            }
        }


class MemberAddReceive(MemberAdd):
    id: int


# Board schemas
class BoardBase(BaseModel):
    title: str

    class Config:
        orm_mode = True


class BoardReceive(BoardBase):
    id: int
    members: List[MemberBase]


class BoardCreate(BoardBase):
    user: int


# User schemas
class UserBase(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class UserReceive(UserBase):
    id: int


class UserCreate(UserBase):
    password: str
