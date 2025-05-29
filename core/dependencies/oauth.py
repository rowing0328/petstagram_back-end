from fastapi import Depends

from Infrastructure.oauth.google_provider import GoogleOAuthProvider
from application.service.member import MemberService
from application.service.oauth import AuthService
from core.dependencies.member import get_member_service

# 싱글톤 GoogleOAuthProvider 객체
google_oauth_provider_singleton = GoogleOAuthProvider()


def get_google_provider() -> GoogleOAuthProvider:
    return google_oauth_provider_singleton


def get_auth_service(
        member_service: MemberService = Depends(get_member_service),
) -> AuthService:
    return AuthService(get_google_provider(), member_service)
