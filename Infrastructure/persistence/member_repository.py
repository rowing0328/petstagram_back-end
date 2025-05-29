from typing import Optional
from sqlmodel import Session, select

from domain.model.user.member import Member
from domain.repository.member_repository_interface import IMemberRepository


class MemberRepository(IMemberRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, member: Member) -> Member:
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def find_by_id(self, member_id: int) -> Optional[Member]:
        statement = select(Member).where(Member.id == member_id, Member.displayed == True)
        result = self.db.exec(statement).first()
        return result

    def find_by_email(self, email: str) -> Optional[Member]:
        statement = select(Member).where(Member.email == email, Member.displayed == True)
        result = self.db.exec(statement).first()
        return result

    def find_by_nickname(self, nickname: str) -> Optional[Member]:
        statement = select(Member).where(Member.nickname == nickname, Member.displayed == True)
        result = self.db.exec(statement).first()
        return result

    def exists_by_email(self, email: str) -> bool:
        statement = select(Member.id).where(Member.email == email)
        result = self.db.exec(statement).first()
        return result is not None
