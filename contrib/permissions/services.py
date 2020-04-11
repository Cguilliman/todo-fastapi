from sqlalchemy.orm import Session

from models import Member
from .consts import MemberPermissions, READ, WRITE, SUPER_WRITE, EDIT, PERMISSIONS


class Permissions(object):

    def __init__(self, db: Session, board_id: int, user_id: int):
        self.db = db
        self.board_id = board_id
        self.user_id = user_id

    def _create_member(self, permissions: MemberPermissions):
        member = Member(
            board_id=self.board_id,
            user_id=self.user_id,
            permissions=permissions,
        )
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def create_owner(self):
        return self._create_member(MemberPermissions.owner)

    def create_member(self):
        return self._create_member(MemberPermissions.member)

    def create_guest(self):
        return self._create_member(MemberPermissions.guest)


class Validator(object):

    def __init__(self, member: Member):
        self.member = member

    def _check_permission(self, permission: int) -> bool:
        return permission in PERMISSIONS.get(self.member.permissions)

    def is_writable(self, is_owner: bool = False) -> bool:
        return (
            self._check_permission(WRITE)
            if is_owner
            else self._check_permission(SUPER_WRITE)
        )

    def is_readable(self) -> bool:
        return self._check_permission(READ)

    def is_editable(self) -> bool:
        return self._check_permission(EDIT)
