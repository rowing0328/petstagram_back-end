from typing import List
from pydantic import Field

from web.payload.request.base_request import BaseRequest


class FeedRegisterRequest(BaseRequest):
    member_id: int = Field(..., description="피드 작성 회원의 고유 ID")
    subject: str = Field(..., description="피드 제목 또는 주제")
    feed_type: str = Field(..., description="피드 타입")
    images: List[str] = Field(..., description="피드에 첨부할 이미지 URL 목록")
    content: str = Field(..., description="피드 본문 내용")
