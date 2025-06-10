from fastapi import Depends

from src.main.python.Infrastructure.config.database import get_session
from src.main.python.Infrastructure.persistence.feed_like_repository import FeedLikeRepository
from src.main.python.application.service.feed_like import FeedLikeService
from src.main.python.core.dependencies.member import get_member_service
from src.main.python.domain.repository.feed_like_interface import IFeedLikeRepository


def get_feed_like_repository(session=Depends(get_session)) -> IFeedLikeRepository:
    return FeedLikeRepository(session)


def get_feed_like_service(
        feed_like_repository: IFeedLikeRepository = Depends(get_feed_like_repository),
        member_service=Depends(get_member_service)
) -> FeedLikeService:
    return FeedLikeService(feed_like_repository, member_service)
