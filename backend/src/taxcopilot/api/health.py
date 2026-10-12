from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from taxcopilot import __version__
from taxcopilot.db import get_session
from taxcopilot.ingestion.registry import all_parsers

router = APIRouter()


@router.get("/health")
def health(session: Annotated[Session, Depends(get_session)]) -> dict[str, Any]:
    row = session.execute(text("SELECT version_num FROM alembic_version")).first()
    return {
        "status": "ok",
        "version": __version__,
        "schema_revision": row[0] if row else None,
        "parsers": sorted(p.id for p in all_parsers()),
        "llm_enabled": False,
    }
