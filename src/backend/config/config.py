# backend/config/config.py
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import ClassVar
import os 
from dotenv import load_dotenv
ENV_FILE = Path("src/.env")
load_dotenv(dotenv_path=ENV_FILE)
class Settings(BaseSettings):
    SECRET_KEY: str
    SESSION_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str

    # ✅ For non-field attributes, use ClassVar
    env_file_encoding: ClassVar[str] = "utf-8"

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()

