from fastapi import Depends

from src.main.python.Infrastructure.oauth.google_provider import GoogleOAuthProvider
from src.main.python.application.service.member import MemberService
from src.main.python.application.service.oauth import AuthService
from src.main.python.core.dependencies.member import get_member_service

# 싱글톤 GoogleOAuthProvider 객체
google_oauth_provider_singleton = GoogleOAuthProvider()


def get_google_provider() -> GoogleOAuthProvider:
    return google_oauth_provider_singleton


def get_auth_service(
        member_service: MemberService = Depends(get_member_service),
) -> AuthService:
    return AuthService(get_google_provider(), member_service)
