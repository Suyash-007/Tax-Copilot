"""Alembic environment. The DB URL comes from app settings (or `-x url=...`), never from alembic.ini."""

from logging.config import fileConfig

from alembic import context
from taxcopilot.db import make_engine
from taxcopilot.models import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

target_metadata = Base.metadata


def run_migrations_online() -> None:
    url = context.get_x_argument(as_dictionary=True).get("url")
    connectable = config.attributes.get("connection") or make_engine(url)
    if hasattr(connectable, "connect"):
        with connectable.connect() as connection:
            _run(connection)
    else:
        _run(connectable)


def _run(connection) -> None:  # type: ignore[no-untyped-def]
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,  # SQLite needs batch mode for ALTER TABLE
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


run_migrations_online()
