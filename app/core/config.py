from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

_DESCRIPTION_FILE = Path(__file__).parent / "description.md"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # API Configuration
    app_name: str = "EcoLogits API"
    app_version: str = "0.0.1beta"
    description: str = _DESCRIPTION_FILE.read_text()

    # CORS Configuration
    allowed_origins: List[str] = ["*"]
    allowed_methods: List[str] = ["*"]
    allowed_headers: List[str] = ["*"]

    # API Configuration
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"


settings = Settings()
