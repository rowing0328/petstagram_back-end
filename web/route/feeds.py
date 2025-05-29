from typing import Optional

from fastapi import APIRouter, Depends, status, Query
from starlette.responses import JSONResponse

from application.service.feed import FeedService
from core.dependencies.feed import get_feed_service
from core.exception.error_message import ErrorMessage
from web.payload.request.feed_register import FeedRegisterRequest
from web.payload.request.feed_update import FeedUpdateRequest
from web.payload.response.base_response import BaseResponse
from web.payload.response.feed_info import FeedInfoResponse
from web.payload.response.feed_list import FeedListResponse

feed_router = APIRouter(tags=["Feed"])


@feed_router.get(
    "/feeds",
    summary="피드 목록 조회 (페이지네이션)",
    response_model=FeedListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "피드 목록 조회 성공",
            "content": {
                "application/json": {
                    "schema": FeedListResponse.schema()
                }
            }
        }
    },
    description="""
    피드 목록 조회 (페이지네이션)

    - 설명: 피드 목록을 페이지네이션으로 조회합니다.
    - 쿼리 파라미터
      - offset: 시작 위치 (기본값: 0)
      - limit: 조회 개수 (기본값: 4)
      - feed_type: 피드 타입 필터 (선택)
      - member_id: 회원 ID로 필터링 (선택)
    - 응답
      - 200: 피드 목록 및 총 개수 반환
    """
)
def get_feeds(
        offset: int = Query(0, description="조회 시작 위치"),
        limit: int = Query(4, description="한 번에 조회할 개수"),
        feed_type: Optional[str] = Query(None, description="피드 타입 필터"),
        member_id: Optional[int] = Query(None, description="회원 ID로 필터"),
        feed_service: FeedService = Depends(get_feed_service)
):
    result = feed_service.paginate(offset, limit, feed_type, member_id)
    return FeedListResponse(
        message="성공",
        total=result["total"],
        feeds=result["feeds"]
    )


@feed_router.get(
    "/feed/{feed_id}",
    summary="피드 상세 조회",
    response_model=FeedInfoResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "피드 상세 정보 반환",
            "content": {
                "application/json": {
                    "schema": FeedInfoResponse.schema()
                }
            }
        },
        400: {
            "description": "피드를 찾을 수 없음",
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
                                "error": ErrorMessage.FEED_NOT_FOUND.value
                            }
                        }
                    }
                }
            }
        }
    },
    description="""
    피드 상세 조회

    - 설명: 피드 ID로 피드 상세 정보를 조회합니다.
    - 경로 파라미터
      - feed_id: 조회할 피드의 ID
    - 쿼리 파라미터
      - member_id: (선택) 피드 좋아요 여부 조회 시 필요
    - 응답
      - 200: 피드 상세 정보 반환
      - 400: 피드를 찾을 수 없음
    """
)
def retrieve(
        feed_id: int,
        member_id: Optional[int] = Query(None, description="(선택) 피드 좋아요 여부 조회 시 필요"),
        feed_service=Depends(get_feed_service)
) -> FeedInfoResponse:
    result = feed_service.view_feed(feed_id, member_id)
    feed = result["feed"]
    has_liked = result["has_liked"]
    return FeedInfoResponse.from_feed(
        feed=feed,
        has_liked=has_liked,
        message="피드 조회 성공",
    )


@feed_router.post(
    "/feed",
    summary="피드 등록 API",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "피드 등록 성공",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string"}
                        }
                    },
                    "example": {
                        "message": "피드 등록 성공"
                    }
                }
            },
            "headers": {
                "Location": {
                    "description": "생성된 피드의 상세 조회 URL",
                    "schema": {"type": "string"}
                }
            }
        },
        400: {
            "description": "회원 정보를 찾을 수 없음",
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
                                "error": ErrorMessage.MEMBER_NOT_FOUND.value
                            }
                        }
                    }
                }
            }
        }
    },
    description="""
    피드 등록 API

    - 설명: 새 피드를 등록합니다.
    - 요청: 회원 ID, 제목, 피드 타입, 이미지, 본문 내용
    - 응답
      - 201: 피드 등록 성공, Location 헤더에 피드 상세 경로 반환
      - 400: 회원 정보를 찾을 수 없음
    """
)
def register(
        request: FeedRegisterRequest,
        feed_service=Depends(get_feed_service)
) -> JSONResponse:
    feed = feed_service.create(request.member_id, request.subject, request.feed_type, request.images, request.content)
    location = f"/feed/{feed.id}"
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "피드 등록 성공"},
        headers={"Location": location},
    )


@feed_router.put(
    "/feed/{feed_id}",
    summary="피드 수정 API",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "피드 수정 성공",
            "content": {
                "application/json": {
                    "schema": BaseResponse.schema()
                }
            }
        },
        400: {
            "description": "피드를 찾을 수 없음",
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
                                "error": ErrorMessage.FEED_NOT_FOUND.value
                            }
                        }
                    }
                }
            }
        }
    },
    description="""
    피드 수정 API

    - 설명: 피드의 제목, 본문, 타입, 이미지 정보를 수정합니다.
    - 경로 파라미터
      - feed_id: 수정할 피드의 ID
    - 요청: 제목, 본문, 피드 타입, 이미지 등
    - 응답
      - 200: 피드 수정 성공
      - 400: 피드를 찾을 수 없음
    """
)
def update(
        feed_id: int,
        request: FeedUpdateRequest,
        feed_service=Depends(get_feed_service)
) -> BaseResponse:
    feed_service.update(
        feed_id=feed_id,
        subject=request.subject,
        content=request.content,
        feed_type=request.feed_type,
        images=request.images,
        contents=request.contents,
    )
    return BaseResponse(message="피드 수정 성공")


@feed_router.delete(
    "/feed/{feed_id}",
    summary="피드 삭제(Soft Delete) API",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "피드 삭제 완료",
            "content": {
                "application/json": {
                    "schema": BaseResponse.schema()
                }
            }
        },
        400: {
            "description": "피드를 찾을 수 없음",
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
                                "error": ErrorMessage.FEED_NOT_FOUND.value
                            }
                        }
                    }
                }
            }
        }
    },
    description="""
    피드 삭제(Soft Delete) API

    - 설명: 피드를 소프트 삭제(비활성화)합니다.
    - 경로 파라미터
      - feed_id: 삭제할 피드의 ID
    - 응답
      - 200: 피드 삭제 완료
      - 400: 피드를 찾을 수 없음
    """
)
def soft_delete(
        feed_id: int,
        feed_service=Depends(get_feed_service)
) -> BaseResponse:
    feed_service.soft_delete(feed_id)
    return BaseResponse(message="피드 삭제 완료")
