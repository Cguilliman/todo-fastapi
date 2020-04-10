from sqlalchemy.orm import Session

from models import Member
from .consts import MemberPermissions


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

    def create_memeber(self):
        return self._create_member(MemberPermissions.member)

    def create_guest(self):
        return self._create_member(MemberPermissions.guest)
