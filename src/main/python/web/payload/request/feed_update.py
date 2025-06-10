from typing import List
from pydantic import Field

from src.main.python.web.payload.request.base_request import BaseRequest


class FeedUpdateRequest(BaseRequest):
    subject: str = Field(..., description="피드 제목 또는 주제")
    feed_type: str = Field(..., description="피드 타입")
    images: List[str] = Field(..., description="피드에 첨부된 이미지 URL 목록")
    content: str = Field(..., description="피드 본문 내용")
