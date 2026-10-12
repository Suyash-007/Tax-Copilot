"""SQLite engine and session factory."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from taxcopilot.config import get_settings


def make_engine(url: str | None = None) -> Engine:
    settings = get_settings()
    if url is None:
        settings.data_dir.mkdir(parents=True, exist_ok=True)
        url = settings.database_url
    engine = create_engine(url)

    @event.listens_for(engine, "connect")
    def _sqlite_pragmas(dbapi_conn: Any, _record: Any) -> None:
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute("PRAGMA journal_mode = WAL")
        cur.close()

    return engine


_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


def get_engine() -> Engine:
    global _engine, _SessionLocal
    if _engine is None:
        _engine = make_engine()
        _SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False)
    return _engine


def get_session() -> Iterator[Session]:
    """FastAPI dependency."""
    get_engine()
    assert _SessionLocal is not None
    with _SessionLocal() as session:
        yield session
