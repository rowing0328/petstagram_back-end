import os
from dotenv import load_dotenv
import httpx

load_dotenv()


class Token:
    def __init__(self, access_token: str):
        self.access_token = access_token


class GoogleOAuthProvider:
    CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

    async def exchange_code_for_token(self, code: str) -> Token:
        TOKEN_URL = "https://oauth2.googleapis.com/token"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TOKEN_URL,
                data={
                    "code": code,
                    "client_id": self.CLIENT_ID,
                    "client_secret": self.CLIENT_SECRET,
                    "redirect_uri": self.GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code"
                }
            )
        response.raise_for_status()
        data = response.json()
        return Token(access_token=data["access_token"])

    async def fetch_user_info(self, access_token: str) -> dict:
        USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
        async with httpx.AsyncClient() as client:
            response = await client.get(
                USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
        response.raise_for_status()
        return response.json()
