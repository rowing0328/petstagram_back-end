from fastapi import APIRouter, Depends, status, Query

from core.dependencies.feed_like import get_feed_like_service
from core.exception.error_message import ErrorMessage
from web.payload.response.base_response import BaseResponse

feed_like_router = APIRouter(prefix="/feed/like", tags=["FeedLike"])


@feed_like_router.post(
    "/{feed_id}",
    summary="피드 좋아요 등록 API",
    status_code=status.HTTP_201_CREATED,
    response_model=BaseResponse,
    responses={
        201: {
            "description": "피드 좋아요 성공",
            "content": {
                "application/json": {
                    "schema": BaseResponse.schema(),
                    "example": {
                        "message": "좋아요 성공"
                    }
                }
            }
        },
        400: {
            "description": "좋아요 등록 실패 (이미 좋아요 또는 회원 없음)",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "error": {"type": "string"}
                        }
                    },
                    "examples": {
                        "user_not_found": {
                            "value": {
                                "error": ErrorMessage.MEMBER_NOT_FOUND.value
                            }
                        },
                        "already_exists": {
                            "value": {
                                "error": ErrorMessage.FEED_LIKE_ALREADY_EXISTS.value
                            }
                        }
                    }
                }
            }
        }
    },
    description="""
    피드 좋아요 등록 API

    - 설명: 피드에 좋아요를 등록합니다.
    - 경로 파라미터
      - feed_id: 좋아요할 피드 ID
    - 쿼리 파라미터
      - member_id: 좋아요를 누르는 회원 ID
    - 응답
      - 201: 좋아요 성공
      - 400: 이미 좋아요를 누른 경우, 회원이 존재하지 않는 경우
    """
)
def register(
        feed_id: int,
        member_id: int = Query(..., description="좋아요를 누르는 회원 ID"),
        feed_like_service=Depends(get_feed_like_service)
) -> BaseResponse:
    feed_like_service.like(feed_id, member_id)
    return BaseResponse(message="좋아요 성공")


@feed_like_router.delete(
    "/{feed_id}",
    summary="피드 좋아요 취소 API",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse,
    responses={
        200: {
            "description": "피드 좋아요 취소 성공",
            "content": {
                "application/json": {
                    "schema": BaseResponse.schema(),
                    "example": {
                        "message": "좋아요 취소 성공"
                    }
                }
            }
        },
        400: {
            "description": "좋아요 취소 실패 (좋아요 정보 없음)",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "error": {"type": "string"}
                        }
                    },
                    "examples": {
                        "not_found": {
                            "value": {
                                "error": ErrorMessage.FEED_LIKE_NOT_FOUND.value
                            }
                        }
                    }
                }
            }
        }
    },
    description="""
    피드 좋아요 취소 API

    - 설명: 피드의 좋아요를 취소합니다.
    - 경로 파라미터
      - feed_id: 좋아요를 취소할 피드 ID
    - 쿼리 파라미터
      - member_id: 좋아요를 취소하는 회원 ID
    - 응답
      - 200: 좋아요 취소 성공
      - 400: 좋아요 정보가 없는 경우
    """
)
def remove(
        feed_id: int,
        member_id: int = Query(..., description="좋아요를 취소하는 회원 ID"),
        feed_like_service=Depends(get_feed_like_service)
) -> BaseResponse:
    feed_like_service.unlike(feed_id, member_id)
    return BaseResponse(message="좋아요 취소 성공")
