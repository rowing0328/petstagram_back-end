import os
from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import RedirectResponse, JSONResponse

from src.main.python.application.service.oauth import AuthService
from src.main.python.core.dependencies.oauth import get_auth_service
from src.main.python.core.exception.error_message import ErrorMessage

auth_router = APIRouter(prefix="/oauth", tags=["OAuth"])


@auth_router.get(
    "/google/login",
    summary="구글 OAuth 로그인 페이지 리다이렉트 API",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    responses={
        307: {
            "description": "구글 OAuth 로그인 페이지로 리다이렉트",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "string",
                        "example": "리다이렉트"
                    }
                }
            }
        }
    },
    description="""
    구글 OAuth 로그인 페이지 리다이렉트 API

    - 설명: 구글 OAuth 인증을 위해 구글 로그인 페이지로 리다이렉트합니다.
    - 응답
      - 307: 구글 로그인 페이지로 리다이렉트
    """
)
async def google_login():
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    scope = "openid email profile"

    url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope={scope.replace(' ', '%20')}"
    )
    return RedirectResponse(url)


@auth_router.get(
    "/google/callback",
    summary="구글 OAuth 로그인 콜백 API",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    responses={
        307: {
            "description": "프론트엔드로 리다이렉트 및 쿠키 세팅",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "string",
                        "example": "리다이렉트"
                    }
                }
            }
        },
        400: {
            "description": "구글 OAuth 인증 실패",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "error": {"type": "string"}
                        }
                    },
                    "examples": {
                        "oauth_failed": {
                            "value": {
                                "error": ErrorMessage.GOOGLE_OAUTH_FAILED.value
                            }
                        }
                    }
                }
            }
        }
    },
    description="""
    구글 OAuth 로그인 콜백 API

    - 설명: 구글 OAuth 인증 후 콜백을 처리하여 회원 인증/가입 및 쿠키(`member_id`, `role`)를 세팅한 후 프론트엔드로 리다이렉트합니다.
    - 쿼리 파라미터
      - code: 구글 OAuth 인증 코드
    - 응답
      - 307: 인증 성공 시 프론트엔드로 리다이렉트 및 쿠키 세팅
      - 400: 인증 실패 (에러 메시지 반환)
    """
)
async def google_callback(
        code: str = Query(..., description="구글 OAuth 인증 코드"),
        auth_service: AuthService = Depends(get_auth_service)
):
    try:
        user_id, role = await auth_service.handle_google_login(code)
        response = RedirectResponse(url="http://localhost:5173")
        response.set_cookie(
            key="member_id", value=str(user_id),
            httponly=True,
            samesite="lax",
            secure=False
        )
        response.set_cookie(
            key="role", value=role,
            httponly=True,
            samesite="lax",
            secure=False
        )
        return response
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": ErrorMessage.GOOGLE_OAUTH_FAILED.value}
        )
