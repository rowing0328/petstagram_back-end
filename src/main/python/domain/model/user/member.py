from typing import Optional
from datetime import datetime, timezone, timedelta

from sqlmodel import SQLModel, Field, Column, String

from src.main.python.core.exception.error_message import ErrorMessage
from src.main.python.domain.model.user.user_authority import UserAuthority


class Member(SQLModel, table=True):
    """
    회원 엔티티 클래스

    Author: 신효승
    Created: 2025-05-23

    Field Description:
    - id: 고유 식별자 (Auto Increment)
    - email: 이메일 (Unique)
    - nickname: 닉네임
    - profile_image: 프로필 이미지 URL
    - password: 비밀번호 (해시된 값)
    - role: 회원 권한 (예: member)
    - displayed: 표시 여부 (소프트 삭제 시 False)
    - created_at: 생성 시각 (KST, 기본값: 현재 시간)
    - updated_at: 수정된 시각 (KST, 기본값: 현재 시간)
    """

    __tablename__ = "members"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column(String(255), nullable=False, unique=True))
    nickname: str = Field(sa_column=Column(String(50), nullable=False))
    profile_image: str = Field(sa_column=Column(String(255), nullable=True))
    password: str = Field(sa_column=Column(String(255), nullable=False))
    animal_name: Optional[str] = Field(default=None, sa_column=Column(String(50), nullable=True))
    role: UserAuthority = Field(nullable=False)
    displayed: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=9))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=9))

    @classmethod
    def check_nickname(cls, nickname):
        if not nickname or not nickname.strip():
            raise ValueError(ErrorMessage.MEMBER_INVALID_NICKNAME.value)

    @classmethod
    def resolve_profile_image(cls, profile_image: Optional[str]) -> str:
        default_url = ""
        return profile_image if profile_image is not None else default_url

    @classmethod
    def create(cls, email: str, nickname: str, profile_image: Optional[str]) -> "Member":
        return cls(
            email=email,
            nickname=nickname,
            profile_image=cls.resolve_profile_image(profile_image),
            role=UserAuthority.member
        )

    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc) + timedelta(hours=9)

    def change_nickname(self, new_nickname: str):
        self.check_nickname(new_nickname)
        self.nickname = new_nickname

    def change_profile_image(self, new_profile_image: str):
        self.profile_image = new_profile_image

    def change_animal_name(self, new_animal_name: Optional[str]):
        self.animal_name = new_animal_name

    def change_displayed(self):
        self.displayed = False
