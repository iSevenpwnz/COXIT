"""Application configuration settings."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings configuration."""
    
    # File constraints
    MAX_FILE_SIZE_MB: int = 50
    MAX_PAGES: int = 100
    
    # OpenAI configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_MAX_TOKENS: int = 800
    OPENAI_TEMPERATURE: float = 0.3
    
    # CORS configuration
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    ALLOWED_ORIGINS: list = [FRONTEND_URL, "http://localhost:3000"]
    
    # Storage paths
    BASE_DIR: Path = Path(__file__).parent.parent
    STORAGE_DIR: Path = BASE_DIR / "storage"
    PDFS_DIR: Path = STORAGE_DIR / "pdfs"
    SUMMARIES_DIR: Path = STORAGE_DIR / "summaries"
    META_DIR: Path = STORAGE_DIR / "meta"
    META_FILE: Path = META_DIR / "metadata.json"
    
    # History settings
    MAX_HISTORY_ITEMS: int = 1000
    HISTORY_DISPLAY_LIMIT: int = 5
    
    def __post_init__(self):
        """Create directories if they don't exist."""
        for directory in [self.PDFS_DIR, self.SUMMARIES_DIR, self.META_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

# Global settings instance
settings = Settings()
settings.__post_init__()