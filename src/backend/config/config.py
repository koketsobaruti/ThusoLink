# backend/config/config.py

from pydantic_settings import BaseSettings
from typing import ClassVar
import os
import secrets
from dotenv import load_dotenv

# Load .env ONLY if it exists (local development)
if os.path.exists(".env"):
    load_dotenv()

class Settings(BaseSettings):
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"

    # Tokens
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SESSION_EXPIRE_MINUTES: int = 60

    # Database
    DATABASE_URL: str

    # WhatsApp / Meta API
    WHATSAPP_PHONE_NUMBER_ID: int
    WHATSAPP_BASE_URL: str
    WHATSAPP_TOKEN: str

    # App credentials
    APP_ID: str
    APP_SECRET: str

    # Messaging
    RECIPIENT_WAID: str
    VERIFY_TOKEN: str
    ACCESS_TOKEN: str
    VERSION: str

    # Config behavior
    env_file_encoding: ClassVar[str] = "utf-8"

    model_config = {
        "extra": "ignore"
    }

# Instantiate settings
settings = Settings()

# Optional: Fail fast if critical variables are missing
required_vars = [
    "DATABASE_URL",
    "SECRET_KEY",
]

for var in required_vars:
    if not getattr(settings, var):
        raise ValueError(f"{var} is not set in environment variables")