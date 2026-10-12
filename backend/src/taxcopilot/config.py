"""Runtime settings. Everything lives under one local data directory; nothing leaves the machine."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TAXCOPILOT_", env_file=".env", extra="ignore")

    data_dir: Path = REPO_ROOT / "data"
    rules_dir: Path = REPO_ROOT / "rules"
    # Bound to loopback only. The frontend proxies /api/* here, so the browser sees one origin.
    host: str = "127.0.0.1"
    port: int = 8000
    # Optional LLM assist is OFF unless explicitly enabled (see docs/PHASE0_PLAN.md §8).
    llm_enabled: bool = False

    @property
    def db_path(self) -> Path:
        return self.data_dir / "taxcopilot.sqlite3"

    @property
    def uploads_dir(self) -> Path:
        return self.data_dir / "uploads"

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.db_path}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
