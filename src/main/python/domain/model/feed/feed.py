from typing import Optional, List
from datetime import datetime, timezone, timedelta

from sqlmodel import SQLModel, Field, Column, JSON, Relationship

from src.main.python.domain.model.feed.feed_type import FeedType


class Feed(SQLModel, table=True):
    """
    Feed 테이블 모델

    Author: 신효승
    Created: 2025-05-24

    Field Description
    - id: 고유 식별자 (AutoIncrement)
    - member_id: 회원 ID (ForeignKey, members.id)
    - feed_type: 타입 (예: FOOD, CARE, MEDICAL, GROOMING)
    - images: 이미지 URL 리스트 (JSON 배열)
    - content: 내용
    - likes: 좋아요 개수
    - views: 조회수
    - displayed: 표시 여부(소프트 삭제 시 False)
    - created_at: 생성 시각 (KST, 기본값: 현재 시간)
    - updated_at: 수정된 시각 (KST, 기본값: 현재 시간)

    Relationship:
    - member: 피드 작성자 (Member와의 관계)
    """

    __tablename__ = "feeds"

    id: Optional[int] = Field(default=None, primary_key=True)
    member_id: int = Field(foreign_key="members.id")
    feed_type: FeedType = Field(nullable=False)
    images: List[str] = Field(sa_column=Column(JSON, nullable=False))
    content: str
    likes: int = Field(default=0, nullable=False)
    views: int = Field(default=0, nullable=False)
    displayed: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=9))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=9))

    member: Optional["Member"] = Relationship()

    @classmethod
    def create(cls, member_id: int, feed_type: str, images: List[str], content: str):
        return cls(
            member_id=member_id,
            feed_type=FeedType.from_value(feed_type),
            images=images,
            content=content
        )

    def change(self, feed_type: str, images: List[str], content: str):
        self.feed_type = FeedType.from_value(feed_type)
        self.images = images
        self.content = content

    def change_displayed(self):
        self.displayed = False

    def increase_views(self):
        self.views += 1
