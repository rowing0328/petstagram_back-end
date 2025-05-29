from fastapi import Depends

from Infrastructure.config.database import get_session
from Infrastructure.persistence.feed_repository import FeedRepository
from application.service.feed import FeedService
from core.dependencies.feed_like import get_feed_like_service
from core.dependencies.file import get_file_service
from core.dependencies.member import get_member_repository
from domain.repository.feed_repository_interface import IFeedRepository
from domain.repository.member_repository_interface import IMemberRepository


def get_feed_repository(session=Depends(get_session)) -> IFeedRepository:
    return FeedRepository(session)


def get_feed_service(
        feed_repository: IFeedRepository = Depends(get_feed_repository),
        member_repository: IMemberRepository = Depends(get_member_repository),
        file_service=Depends(get_file_service),
        feed_like_service=Depends(get_feed_like_service)
) -> FeedService:
    return FeedService(feed_repository, member_repository, file_service, feed_like_service)
