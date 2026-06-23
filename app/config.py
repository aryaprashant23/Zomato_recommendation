import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Groq API Configuration
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_TEMPERATURE: float = 0.3

    # Application Settings
    DATASET_CACHE_PATH: str = "data/zomato_cache.parquet"
    MAX_CANDIDATES: int = 20
    TOP_K: int = 5

    # Base directory of the project
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # Configuration for loading from .env
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
