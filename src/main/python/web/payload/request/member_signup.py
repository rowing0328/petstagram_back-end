from typing import Optional
from pydantic import Field

from src.main.python.web.payload.request.base_request import BaseRequest


class MemberSignUpRequest(BaseRequest):
    email: str = Field(..., description="회원 이메일 (필수)")
    nickname: str = Field(..., description="회원 닉네임 (필수)")
    profile_image: Optional[str] = Field(None, description="회원 프로필 이미지 URL (선택 입력)")
