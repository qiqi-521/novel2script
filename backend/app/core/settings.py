"""Application settings loaded from environment variables."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    openai_base_url: str
    openai_model: str
    openai_timeout_seconds: float

    @property
    def ai_enabled(self) -> bool:
        return bool(self.openai_api_key and self.openai_model)


def get_settings() -> Settings:
    timeout = os.getenv("OPENAI_TIMEOUT_SECONDS", "30")
    try:
        timeout_seconds = float(timeout)
    except ValueError:
        timeout_seconds = 30.0

    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        openai_timeout_seconds=timeout_seconds,
    )
