from typing import Optional
from abc import ABC, abstractmethod

from src.main.python.domain.model.user.member import Member


class IMemberRepository(ABC):
    @abstractmethod
    def save(self, member: Member) -> Member:
        pass

    @abstractmethod
    def find_by_id(self, member_id: int) -> Optional[Member]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Member]:
        pass

    @abstractmethod
    def find_by_nickname(self, nickname: str) -> Optional[Member]:
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass
