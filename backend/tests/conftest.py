from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient

from alembic import command

BACKEND_DIR = Path(__file__).resolve().parents[1]


def alembic_config() -> Config:
    return Config(str(BACKEND_DIR / "alembic.ini"))


@pytest.fixture
def data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    """Point the app at a throwaway data dir and reset cached settings/engine around each test."""
    import taxcopilot.db as db
    from taxcopilot.config import get_settings

    monkeypatch.setenv("TAXCOPILOT_DATA_DIR", str(tmp_path))
    get_settings.cache_clear()
    db._engine, db._SessionLocal = None, None
    yield tmp_path
    if db._engine is not None:
        db._engine.dispose()
    db._engine, db._SessionLocal = None, None
    get_settings.cache_clear()


@pytest.fixture
def migrated_db(data_dir: Path) -> Path:
    command.upgrade(alembic_config(), "head")
    return data_dir / "taxcopilot.sqlite3"


@pytest.fixture
def client(migrated_db: Path) -> TestClient:
    from taxcopilot.main import create_app

    return TestClient(create_app(), base_url="http://127.0.0.1")
