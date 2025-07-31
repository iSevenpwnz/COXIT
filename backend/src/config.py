"""Application configuration settings."""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()


class Settings:
    """Application settings configuration."""

    MAX_FILE_SIZE_MB: int = 50
    MAX_PAGES: int = 100

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_MAX_TOKENS: int = 800
    OPENAI_TEMPERATURE: float = 0.3

    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    ALLOWED_ORIGINS: List[str] = [FRONTEND_URL, "http://localhost:3000"]

    ENABLE_CACHING: bool = (
        os.getenv("ENABLE_CACHING", "true").lower() == "true"
    )
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    BASE_DIR: Path = Path(__file__).parent.parent
    STORAGE_DIR: Path = BASE_DIR / "storage"
    PDFS_DIR: Path = STORAGE_DIR / "pdfs"
    SUMMARIES_DIR: Path = STORAGE_DIR / "summaries"
    META_DIR: Path = STORAGE_DIR / "meta"
    META_FILE: Path = META_DIR / "metadata.json"

    MAX_HISTORY_ITEMS: int = 1000
    HISTORY_DISPLAY_LIMIT: int = 5

    def __post_init__(self):
        """Create directories if they don't exist."""
        for directory in [self.PDFS_DIR, self.SUMMARIES_DIR, self.META_DIR]:
            directory.mkdir(parents=True, exist_ok=True)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    settings = Settings()
    settings.__post_init__()
    return settings


settings = get_settings()
