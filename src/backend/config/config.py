# backend/config/config.py
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import ClassVar
import os 
import secrets
from dotenv import load_dotenv
ENV_FILE = Path(__file__).resolve().parent.parent.parent.parent / ".env"
# import logger
print(f"Loading environment variables from: {ENV_FILE}")
load_dotenv(dotenv_path=ENV_FILE)
class Settings(BaseSettings):
    # SECRET_KEYs: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SESSION_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    # ✅ For non-field attributes, use ClassVar
    env_file_encoding: ClassVar[str] = "utf-8"

    model_config = {
        "env_file": str(ENV_FILE),
        "extra": "ignore"
    }

settings = Settings()

