from typing import List
from pydantic import Field

from src.main.python.web.payload.response.base_response import BaseResponse
from src.main.python.web.payload.response.feed_list_item import FeedListItemResponse


class FeedListResponse(BaseResponse):
    total: int = Field(..., description="전체 피드의 개수")
    feeds: List[FeedListItemResponse] = Field(..., description="피드 목록 (FeedListItemResponse 리스트)")
