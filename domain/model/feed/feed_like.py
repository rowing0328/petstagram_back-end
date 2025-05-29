from typing import Optional
from datetime import datetime, timezone, timedelta

from sqlmodel import SQLModel, Field, UniqueConstraint


class FeedLike(SQLModel, table=True):
    """
    Feed Like 테이블 모델

    Author: 신효승
    Created: 2025-05-25

    Description:
    - feed_likes 테이블은 피드에 대한 회원의 좋아요 기록을 저장합니다.
    - 하나의 회원이 같은 피드에 중복으로 좋아요를 남길 수 없도록 feed_id, member_id에 유니크 제약조건이 있습니다.

    Field Description:
    - id: 고유 식별자 (AutoIncrement)
    - feed_id: 피드 ID (ForeignKey, feeds.id)
    - member_id: 회원 ID (ForeignKey, members.id)
    - created_at: 생성 시각 (KST, 기본값: 현재 시간)
    """
    __tablename__ = "feed_likes"
    __table_args__ = (
        UniqueConstraint("feed_id", "member_id", name="uq_feed_member"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    feed_id: int = Field(nullable=False, foreign_key="feeds.id")
    member_id: int = Field(nullable=False, foreign_key="members.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=9))

    @classmethod
    def create(cls, feed_id: int, member_id: int) -> "FeedLike":
        return cls(
            feed_id=feed_id,
            member_id=member_id,
        )
