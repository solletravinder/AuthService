from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    REDIRECT_URI: str = ""
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: str = ""
    DATABASE_URL: str = ""
    DOMAIN: str = ""
    COOKIE_DOMAIN: str = ""
    COOKIE_SECURE: str = "False"
    GLOBAL_PATH: str = os.path.abspath(os.path.dirname(__file__))

    class Config:
        env_file = ".env"

settings = Settings()
