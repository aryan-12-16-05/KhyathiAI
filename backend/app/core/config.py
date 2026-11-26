
from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


# ==========================================
# PROJECT PATHS
# ==========================================

BACKEND_ROOT = Path(__file__).resolve().parents[2]

ENV_FILE = BACKEND_ROOT / ".env"


# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

class Settings(BaseSettings):

    # Application metadata
    app_name: str = "KhyathiAI API"
    app_version: str = "0.1.0"
    app_environment: str = "development"

    # API configuration
    api_v1_prefix: str = "/api/v1"

    # Frontend configuration
    frontend_origins: list[str] = [
        "http://localhost:5173"
    ]

    # OpenRouter configuration
    openrouter_base_url: str = (
        "https://openrouter.ai/api/v1"
    )

    openrouter_model: str = (
        "nvidia/nemotron-3-ultra-550b-a55b:free"
    )

    openrouter_api_key: SecretStr | None = None

    # Environment variable configuration
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# ==========================================
# SETTINGS INSTANCE
# ==========================================

@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached application settings instance.
    """

    return Settings()


settings = get_settings()
