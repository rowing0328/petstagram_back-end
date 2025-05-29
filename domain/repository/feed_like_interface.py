from abc import ABC, abstractmethod
from typing import Optional

from domain.model.feed.feed_like import FeedLike


class IFeedLikeRepository(ABC):
    @abstractmethod
    def save(self, feed_like: FeedLike) -> FeedLike:
        pass

    @abstractmethod
    def delete(self, feed_like_id: int):
        pass

    @abstractmethod
    def find_by_feed_id_and_member_id(self, feed_id: int, member_id: int) -> Optional[FeedLike]:
        pass

    @abstractmethod
    def exists_by_feed_id_and_member_id(self, feed_id: int, member_id: int) -> bool:
        pass

    @abstractmethod
    def count_by_feed_id(self, feed_id: int) -> int:
        pass
