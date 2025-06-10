from fastapi import Depends

from src.main.python.Infrastructure.config.database import get_session
from src.main.python.Infrastructure.persistence.member_repository import MemberRepository
from src.main.python.application.service.member import MemberService
from src.main.python.core.dependencies.file import get_file_service
from src.main.python.domain.repository.member_repository_interface import IMemberRepository


def get_member_repository(session=Depends(get_session)) -> IMemberRepository:
    return MemberRepository(session)


# 싱글톤 MemberService 객체는 불가 (repository가 매번 달라짐)
def get_member_service(
        member_repository: IMemberRepository = Depends(get_member_repository),
        file_service=Depends(get_file_service)
) -> MemberService:
    return MemberService(member_repository, file_service)
