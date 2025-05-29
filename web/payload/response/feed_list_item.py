from pydantic import BaseModel, Field


class FeedListItemResponse(BaseModel):
    has_liked: bool = Field(..., description="현재 사용자가 해당 피드를 좋아요 했는지 여부")
    author_nickname: str = Field(..., description="피드 작성자의 닉네임")
    author_profile_image: str = Field(..., description="피드 작성자의 프로필 이미지 URL")
    feed_id: int = Field(..., description="피드의 고유 ID")
    feed_type: str = Field(..., description="피드 타입")
    subject: str = Field(..., description="피드 제목 또는 주제")
    image: str = Field(..., description="피드에 첨부된 이미지 URL")
    content: str = Field(..., description="피드 본문 내용")
    likes: int = Field(..., description="피드의 좋아요 수")
    views: int = Field(..., description="피드의 조회수")
    created_at: str = Field(..., description="피드 생성 일시 (ISO 8601 형식)")
