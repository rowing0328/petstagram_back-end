from pydantic import Field

from domain.model.user.member import Member
from web.payload.response.base_response import BaseResponse


class MemberInfoResponse(BaseResponse):
    member_id: int = Field(..., description="회원 고유 ID")
    email: str = Field(..., description="회원 이메일")
    nickname: str = Field(..., description="회원 닉네임")
    profile_image: str = Field(..., description="회원 프로필 이미지 URL")

    @classmethod
    def from_member(cls, member: Member, message: str) -> "MemberInfoResponse":
        return cls(
            message=message,
            member_id=member.id,
            email=member.email,
            nickname=member.nickname,
            profile_image=member.profile_image,
        )
