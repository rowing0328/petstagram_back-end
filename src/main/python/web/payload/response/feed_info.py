from typing import List
from pydantic import Field

from src.main.python.domain.model.feed.feed import Feed
from src.main.python.web.payload.response.base_response import BaseResponse


class FeedInfoResponse(BaseResponse):
    has_liked: bool = Field(..., description="현재 사용자가 해당 피드를 좋아요 했는지 여부")
    author_nickname: str = Field(..., description="피드 작성자의 닉네임")
    author_profile_image: str = Field(..., description="피드 작성자의 프로필 이미지 URL")
    feed_id: int = Field(..., description="피드 고유 ID")
    feed_type: str = Field(..., description="피드 타입")
    images: List[str] = Field(..., description="피드에 첨부된 이미지 URL 목록")
    content: str = Field(..., description="피드 본문 내용")
    likes: int = Field(..., description="피드의 좋아요 수")
    views: int = Field(..., description="피드의 조회수")
    created_at: str = Field(..., description="피드 생성 일시 (ISO 8601 형식)")

    @classmethod
    def from_feed(cls, feed: Feed, has_liked: bool, message: str) -> "FeedInfoResponse":
        return cls(
            message=message,
            has_liked=has_liked,
            author_nickname=feed.member.nickname,
            author_profile_image=feed.member.profile_image,
            feed_id=feed.id,
            feed_type=feed.feed_type.value.lower(),
            images=feed.images,
            content=feed.content,
            likes=feed.likes,
            views=feed.views,
            created_at=feed.created_at.isoformat(),
        )
