from typing import List
from pydantic import BaseModel
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


class MemberBase(Editable):
    id: int
    permissions: MemberPermissions

    # class Config:
    #     orm_mode = True

    def get_permissions(self):
        print(MemberPermissions.get_label(self.permissions))
        return MemberPermissions.get_label(self.permissions)


class BoardBase(BaseModel):
    title: str

    class Config:
        orm_mode = True


class BoardReceive(BoardBase):
    id: int
    members: List[MemberBase]


class BoardCreate(BoardBase):
    user: int


class UserBase(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class UserReceive(UserBase):
    id: int


class UserCreate(UserBase):
    password: str
