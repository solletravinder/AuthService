from authlib.integrations.httpx_client import AsyncOAuth2Client
from config import settings

async def get_oauth_client(provider: str):
    if provider == "google":
        return AsyncOAuth2Client(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=settings.REDIRECT_URI,
            authorize_url="https://accounts.google.com/o/oauth2/auth",
            access_token_url="https://oauth2.googleapis.com/token",
            userinfo_endpoint="https://www.googleapis.com/oauth2/v3/userinfo",
        )
    raise NotImplementedError(f"Provider {provider} not supported")
