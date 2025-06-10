from src.main.python.application.service.member import MemberService
from src.main.python.core.exception.error_message import ErrorMessage
from src.main.python.domain.model.feed.feed_like import FeedLike
from src.main.python.domain.repository.feed_like_interface import IFeedLikeRepository


class FeedLikeService:
    def __init__(self, feed_like_repository: IFeedLikeRepository, member_service: MemberService):
        self.feed_like_repository = feed_like_repository
        self.member_service = member_service

    def like(self, feed_id: int, member_id: int) -> FeedLike:
        self.member_service.find_by_id(member_id)
        if self.exists_by_feed_id_and_member_id(feed_id, member_id):
            raise ValueError(ErrorMessage.FEED_LIKE_ALREADY_EXISTS.value)
        feed_like = FeedLike.create(feed_id=feed_id, member_id=member_id)
        return self.feed_like_repository.save(feed_like)

    def unlike(self, feed_id: int, member_id: int):
        feed_like = self.find_by_feed_id_and_member_id(feed_id, member_id)
        return self.feed_like_repository.delete(feed_like)

    def find_by_feed_id_and_member_id(self, feed_id: int, member_id: int) -> FeedLike:
        feed_like = self.feed_like_repository.find_by_feed_id_and_member_id(feed_id, member_id)
        if feed_like is None:
            raise ValueError(ErrorMessage.FEED_LIKE_NOT_FOUND.value)
        return feed_like

    def exists_by_feed_id_and_member_id(self, feed_id: int, member_id: int) -> bool:
        return self.feed_like_repository.exists_by_feed_id_and_member_id(feed_id, member_id)

    def count(self, feed_id: int) -> int:
        return self.feed_like_repository.count_by_feed_id(feed_id)
