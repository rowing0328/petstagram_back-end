from typing import Optional
from pydantic import Field

from src.main.python.web.payload.request.base_request import BaseRequest


class MemberUpdateRequest(BaseRequest):
    nickname: Optional[str] = Field(None, description="수정할 닉네임 (선택 입력)")
    profile_image: Optional[str] = Field(None, description="수정할 프로필 이미지 URL (선택 입력)")
    animal_name: Optional[str] = Field(None, description="수정할 반려동물 이름 (선택 입력)")
