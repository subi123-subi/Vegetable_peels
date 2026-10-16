import os
from pathlib import Path
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base backend directory: d:\Pattent project 02\backend
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Peel AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "smart-peel-ai-dev-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    DATABASE_URL: str = f"sqlite:///{BACKEND_DIR / 'smart_peel_ai.db'}"

    # CORS
    ALLOWED_ORIGINS: Union[str, List[str]] = "http://localhost,http://localhost:3000,http://localhost:8000,http://localhost:8080"

    # Storage & AI
    UPLOAD_DIR: str = str(BACKEND_DIR / "uploads")
    MODEL_PATH: str = str(BACKEND_DIR.parent / "ai" / "models" / "smart_peel_mobilenetv3.keras")
    CONFIDENCE_THRESHOLD: float = 0.65

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def resolve_sqlite_path(cls, v: str) -> str:
        if v and v.startswith("sqlite:///./"):
            relative_part = v.replace("sqlite:///./", "")
            resolved_path = (BACKEND_DIR / relative_part).as_posix()
            return f"sqlite:///{resolved_path}"
        return v

    @property
    def cors_origins(self) -> List[str]:
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]
        return self.ALLOWED_ORIGINS

    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )


settings = Settings()
