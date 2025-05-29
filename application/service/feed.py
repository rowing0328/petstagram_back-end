from typing import List, Optional, Dict, Any

from domain.repository.feed_repository_interface import IFeedRepository
from domain.repository.member_repository_interface import IMemberRepository
from application.service.feed_like import FeedLikeService
from application.service.file import FileService
from core.exception.error_message import ErrorMessage
from domain.model.feed.feed import Feed


class FeedService:
    _FEED_IMAGE_CONTEXT = "feed"

    def __init__(self, feed_repository: IFeedRepository, member_repository: IMemberRepository,
                 file_service: FileService, feed_like_service: FeedLikeService):
        self.feed_repository = feed_repository
        self.member_repository = member_repository
        self.file_service = file_service
        self.feed_like_service = feed_like_service

    def create(self, member_id: int, subject: str, feed_type: str, images: List[str], content: str) -> Feed:
        self.member_repository.find_by_id(member_id)

        confirmed_images = []
        for image_path in images:
            moved_path = self.file_service.confirm(image_path, self._FEED_IMAGE_CONTEXT)
            confirmed_images.append(moved_path)

        feed = Feed.create(member_id, subject, feed_type, confirmed_images, content)
        return self.feed_repository.save(feed)

    def update(self, feed_id: int, subject: str, feed_type: str, images: List[str], content: str) -> Feed:
        feed = self.feed_repository.find_by_id(feed_id)
        feed.change(subject, feed_type, images, content)
        return self.feed_repository.save(feed)

    def soft_delete(self, feed_id: int) -> Feed:
        feed = self.feed_repository.find_by_id(feed_id)
        feed.change_displayed()
        return feed

    def find_by_id(self, feed_id: int) -> Optional[Feed]:
        feed = self.feed_repository.find_by_id(feed_id)
        if feed is None:
            raise ValueError(ErrorMessage.FEED_NOT_FOUND.value)
        return feed

    def view_feed(self, feed_id: int, member_id: Optional[int] = None) -> dict:
        feed = self.find_by_id(feed_id)
        feed.increase_views()
        self.feed_repository.save(feed)
        has_liked = bool(member_id and self.feed_like_service.exists_by_feed_id_and_member_id(feed_id, member_id))
        return {"feed": feed, "has_liked": has_liked}

    def paginate(self, offset: int, limit: int, feed_type: Optional[str] = None, member_id: Optional[int] = None) -> \
    Dict[str, Any]:
        feeds = self.feed_repository.paginate(offset, limit, feed_type, member_id)
        total = self.feed_repository.count(feed_type, member_id)

        items = []
        for feed in feeds:
            image = feed.images[0]
            has_liked = False
            if member_id:
                has_liked = self.feed_like_service.exists_by_feed_id_and_member_id(feed.id, member_id)

            # 필드 순서/명 맞추기
            items.append({
                "has_liked": bool(has_liked),
                "author_nickname": feed.member.nickname,
                "author_profile_image": feed.member.profile_image,
                "feed_id": feed.id,
                "feed_type": feed.feed_type.value.lower(),
                "subject": feed.subject,
                "image": image,
                "content": feed.content,
                "likes": feed.likes,
                "views": feed.views,
                "created_at": feed.created_at.isoformat(),
            })

        return {"total": total, "feeds": items}
