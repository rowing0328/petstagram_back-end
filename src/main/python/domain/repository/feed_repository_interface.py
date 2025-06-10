from typing import Optional, List
from abc import ABC, abstractmethod

from src.main.python.domain.model.feed.feed import Feed


class IFeedRepository(ABC):
    @abstractmethod
    def save(self, feed: Feed) -> Feed:
        pass

    @abstractmethod
    def find_by_id(self, feed_id: int) -> Optional[Feed]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[Feed]:
        pass

    @abstractmethod
    def paginate(self, offset: int, limit: int, feed_type: Optional[str] = None, member_id: Optional[int] = None) -> List[Feed]:
        pass

    @abstractmethod
    def count(self, feed_type: Optional[str], member_id: Optional[str]) -> int:
        pass
