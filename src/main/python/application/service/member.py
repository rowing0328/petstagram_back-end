from typing import Optional

from src.main.python.application.service.file import FileService
from src.main.python.core.exception.error_message import ErrorMessage
from src.main.python.domain.model.user.member import Member
from src.main.python.domain.repository.member_repository_interface import IMemberRepository


class MemberService:
    _MEMBER_IMAGE_CONTEXT = "member"

    def __init__(self, member_repository: IMemberRepository, file_service: FileService):
        self.repository = member_repository
        self.file_service = file_service

    def create(self, email: str, nickname: str, profile_image: Optional[str]) -> Member:
        # 닉네임 중복 체크
        if self.repository.exists_by_email(email):
            raise ValueError(ErrorMessage.MEMBER_EMAIL_DUPLICATE.value)
        member = Member.create(email, nickname, profile_image)
        return self.repository.save(member)

    def update(self, member_id: int, nickname: str, profile_image: str, animal_name: str) -> Member:
        member = self.repository.find_by_id(member_id)
        if nickname and nickname != member.nickname:
            if self.repository.find_by_nickname(nickname):
                raise ValueError(ErrorMessage.MEMBER_NICKNAME_DUPLICATE.value)
            member.change_nickname(nickname)
        if profile_image is not None:
            member.change_profile_image(profile_image)
            self.file_service.confirm(profile_image, self._MEMBER_IMAGE_CONTEXT)
        if animal_name is not None:
            member.change_animal_name(animal_name)
        member.update_timestamp()
        return self.repository.save(member)

    def soft_delete(self, member_id: int) -> Member:
        member = self.repository.find_by_id(member_id)
        member.change_displayed()
        return self.repository.save(member)

    def find_by_id(self, member_id: int) -> Optional[Member]:
        member = self.repository.find_by_id(member_id)
        if member is None:
            raise ValueError(ErrorMessage.MEMBER_NOT_FOUND.value)
        return member

    def find_by_email(self, email: str) -> Optional[Member]:
        member = self.repository.find_by_email(email)
        if member is None:
            raise ValueError(ErrorMessage.MEMBER_NOT_FOUND.value)
        return member

    def find_by_nickname(self, nickname: str) -> Optional[Member]:
        member = self.repository.find_by_nickname(nickname)
        if member is None:
            raise ValueError(ErrorMessage.MEMBER_NOT_FOUND.value)
        return member

    def exists_by_email(self, email: str) -> bool:
        return self.repository.exists_by_email(email)
