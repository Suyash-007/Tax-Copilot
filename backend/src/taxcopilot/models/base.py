from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any

from sqlalchemy import JSON, DateTime, Enum, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from taxcopilot.db_types import DecimalText, utcnow

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)
    type_annotation_map = {  # noqa: RUF012 - SQLAlchemy reads this class attribute
        Decimal: DecimalText(),
        datetime: DateTime(),
        dict[str, Any]: JSON,
        list[Any]: JSON,
    }


def str_enum(enum_cls: type[StrEnum]) -> Enum:
    """Enum stored by value as VARCHAR with no CHECK constraint (see models/enums.py)."""
    return Enum(
        enum_cls,
        native_enum=False,
        create_constraint=False,
        length=32,
        values_callable=lambda e: [m.value for m in e],
    )


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
