from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse

from core.dependencies.member import get_member_service
from core.exception.error_message import ErrorMessage
from web.payload.request.member_signup import MemberSignUpRequest
from web.payload.request.member_update import MemberUpdateRequest
from web.payload.response.base_response import BaseResponse
from web.payload.response.member_info import MemberInfoResponse

member_router = APIRouter(prefix="/member", tags=["Member"])


@member_router.get(
    "/me",
    response_model=MemberInfoResponse,
    summary="내 정보(로그인 상태) 조회 API",
    status_code=status.HTTP_200_OK,
    responses={
        401: {
            "description": "로그인 필요",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {"error": {"type": "string"}}
                    },
                    "examples": {
                        "not_logged_in": {
                            "value": {
                                "error": ErrorMessage.AUTH_NOT_LOGGED_IN.value
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "회원 정보를 찾을 수 없음",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {"error": {"type": "string"}}
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
    내 정보(로그인 상태) 조회 API

    - 설명: 현재 로그인한 사용자의 정보를 조회합니다.
    - 쿠키: `member_id`를 사용하여 로그인 여부를 확인합니다.
    - 응답
      - 200: 회원 정보 반환
      - 400: 회원 정보를 찾을 수 없음
      - 401: 로그인 필요
    """
)
def retrieve_my_info(
        request: Request,
        member_service=Depends(get_member_service)
) -> MemberInfoResponse:
    member_id = request.cookies.get("member_id")
    if not member_id:
        raise PermissionError(ErrorMessage.AUTH_NOT_LOGGED_IN)
    member = member_service.find_by_id(int(member_id))
    return MemberInfoResponse.from_member(
        member=member,
        message="로그인 상태 조회 성공"
    )


@member_router.get(
    "/{member_id}",
    response_model=MemberInfoResponse,
    summary="내 정보 조회 API",
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "error": {"type": "string"}
                        }
                    },
                    "example": {
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
    내 정보 조회 API

    - 설명: 현재 로그인한 사용자의 정보를 반환합니다.
    - 쿠키: `member_id`를 사용해 로그인 여부를 확인합니다.
    - 응답
      - 200: 회원 정보 반환
      - 400: 회원 정보를 찾을 수 없음
    """
)
def retrieve(
        member_id: int,
        member_service=Depends(get_member_service)
) -> MemberInfoResponse:
    member = member_service.find_by_id(member_id)
    return MemberInfoResponse.from_member(
        member=member,
        message="회원 조회 성공"
    )


@member_router.post(
    "",
    summary="회원가입 API",
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "description": "이메일 중복 또는 잘못된 요청",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {"error": {"type": "string"}}
                    },
                    "examples": {
                        "duplicate": {
                            "value": {
                                "error": ErrorMessage.MEMBER_EMAIL_DUPLICATE.value
                            }
                        }
                    }
                }
            }
        }
    },
    description="""
    회원가입 API

    - 설명: 신규 회원을 등록합니다.
    - 요청: 이메일, 닉네임, 프로필 이미지를 입력합니다.
    - 응답
      - 201: 회원가입 성공 및 Location 헤더로 회원 정보 URL 반환
      - 400: 이메일 중복 또는 잘못된 요청
    """
)
def register(
        request: MemberSignUpRequest,
        member_service=Depends(get_member_service)
) -> JSONResponse:
    member = member_service.create(request.email, request.nickname, request.profile_image)
    location = f"/member/{member.id}"
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "회원가입 성공"},
        headers={"Location": location}
    )


@member_router.patch(
    "/{member_id}",
    response_model=BaseResponse,
    summary="회원 정보 수정 API",
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "description": "회원 정보 수정 실패",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {"error": {"type": "string"}}
                    },
                    "examples": {
                        "not_found": {
                            "value": {
                                "error": ErrorMessage.MEMBER_NOT_FOUND.value
                            }
                        },
                        "invalid": {
                            "value": {
                                "error": ErrorMessage.MEMBER_INVALID_NICKNAME.value
                            }
                        }
                    }
                }
            }
        }
    },
    description="""
    회원 정보 수정 API

    - 설명: 회원의 닉네임, 프로필 이미지를 수정합니다.
    - 요청: 닉네임, 프로필 이미지
    - 응답
      - 200: 회원 정보 수정 성공
      - 400: 회원 정보를 찾을 수 없음 또는 잘못된 닉네임
    """
)
def modify(
        member_id: int,
        request: MemberUpdateRequest,
        member_service=Depends(get_member_service)
) -> BaseResponse:
    member_service.update(member_id, request.nickname, request.profile_image)
    return BaseResponse(message="회원 정보 수정 성공")


@member_router.delete(
    "/{member_id}",
    response_model=BaseResponse,
    summary="회원 탈퇴(비활성화) API",
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "description": "회원 정보를 찾을 수 없음",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {"error": {"type": "string"}}
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
    회원 탈퇴(비활성화) API

    - 설명: 회원의 계정을 비활성화(탈퇴) 처리합니다.
    - 응답
      - 200: 회원 탈퇴(비활성화) 완료
      - 400: 회원 정보를 찾을 수 없음
    """
)
def remove(
        member_id: int,
        member_service=Depends(get_member_service)
) -> BaseResponse:
    member_service.soft_delete(member_id)
    return BaseResponse(message="회원 탈퇴(비활성화) 완료")
