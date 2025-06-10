from typing import Optional, List

from sqlmodel import Session, select, func

from src.main.python.domain.model.feed.feed import Feed
from src.main.python.domain.repository.feed_repository_interface import IFeedRepository


class FeedRepository(IFeedRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, feed: Feed) -> Feed:
        self.db.add(feed)
        self.db.commit()
        self.db.refresh(feed)
        return feed

    def find_by_id(self, feed_id: int) -> Optional[Feed]:
        statement = select(Feed).where(Feed.id == feed_id, Feed.displayed == True)
        result = self.db.exec(statement).first()
        return result

    def find_by_user_id(self, user_id: int) -> Optional[Feed]:
        statement = select(Feed).where(Feed.user_id == user_id, Feed.displayed == True)
        result = self.db.exec(statement).first()
        return result

    def paginate(self, offset: int, limit: int, feed_type: Optional[str] = None, member_id: Optional[int] = None) -> List[Feed]:
        statement = select(Feed).where(Feed.displayed == True)
        if feed_type:
            statement = statement.where(Feed.type == feed_type)
        if member_id:
            statement = statement.where(Feed.user_id == member_id)
        statement = statement.offset(offset).limit(limit).order_by(Feed.created_at.desc())
        results = self.db.exec(statement)
        return results

    def count(self, feed_type: Optional[str], member_id: Optional[str]) -> int:
        statement = select(func.count()).select_from(Feed).where(Feed.displayed == True)
        if feed_type:
            statement = statement.where(Feed.feed_type == feed_type)
        if member_id:
            statement = statement.where(Feed.member_id == member_id)
        total = self.db.exec(statement).one()
        return total[0] if isinstance(total, tuple) else total
