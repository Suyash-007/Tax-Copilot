from pathlib import Path

from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, inspect

from taxcopilot.models import Base


def test_migrations_match_models(migrated_db: Path) -> None:
    """If this fails, a model changed without a migration: run `make db-revision m="..."`."""
    engine = create_engine(f"sqlite:///{migrated_db}")
    with engine.connect() as conn:
        diff = compare_metadata(MigrationContext.configure(conn), Base.metadata)
    assert diff == []


def test_core_tables_exist(migrated_db: Path) -> None:
    tables = set(inspect(create_engine(f"sqlite:///{migrated_db}")).get_table_names())
    for t in (
        "account",
        "source_file",
        "raw_row",
        "txn",
        "link",
        "link_leg",
        "category_assignment",
        "lot",
        "disposal",
        "tax_computation_line",
        "tax_line_source",
    ):
        assert t in tables
