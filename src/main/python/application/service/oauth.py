from src.main.python.Infrastructure.oauth.google_provider import GoogleOAuthProvider
from src.main.python.application.service.member import MemberService


class AuthService:
    def __init__(self, google_provider: GoogleOAuthProvider, member_service: MemberService):
        self.google_manager = google_provider
        self.member_service = member_service

    async def handle_google_login(self, code: str):
        token = await self.google_manager.exchange_code_for_token(code)

        userinfo = await self.google_manager.fetch_user_info(token.access_token)
        email = userinfo.get('email')

        if not self.member_service.exists_by_email(email):
            self.member_service.create(email, userinfo.get("name"), userinfo.get("picture"))

        member = self.member_service.find_by_email(email)
        return member.id, member.role.name.lower()
