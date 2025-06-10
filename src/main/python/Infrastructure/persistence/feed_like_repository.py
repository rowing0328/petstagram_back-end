from typing import Optional

from sqlmodel import Session, select, func

from src.main.python.domain.model.feed.feed_like import FeedLike
from src.main.python.domain.repository.feed_like_interface import IFeedLikeRepository


class FeedLikeRepository(IFeedLikeRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, feed_like: FeedLike) -> FeedLike:
        self.db.add(feed_like)
        self.db.commit()
        self.db.refresh(feed_like)
        return feed_like

    def delete(self, feed_like: FeedLike):
        self.db.delete(feed_like)
        self.db.commit()

    def find_by_feed_id_and_member_id(self, feed_id: int, member_id: int) -> Optional[FeedLike]:
        statement = select(FeedLike).where(FeedLike.feed_id == feed_id, FeedLike.member_id == member_id)
        return self.db.exec(statement).first()

    def exists_by_feed_id_and_member_id(self, feed_id: int, member_id: int) -> bool:
        statement = select(FeedLike.id).where(FeedLike.feed_id == feed_id,FeedLike.member_id == member_id)
        result = self.db.exec(statement).first() is not None
        return result

    def count_by_feed_id(self, feed_id: int) -> int:
        statement = select(func.count()).select_from(FeedLike).where(FeedLike.feed_id == feed_id)
        result = self.db.exec(statement).scalar_one()
        return result
