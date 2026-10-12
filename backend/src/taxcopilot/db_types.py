"""Column types that keep numbers exact.

Money is always an integer count of minor units (paise for INR, cents for USD) in a BigInteger
column. Non-money decimals (quantities, NAVs, prices, FX rates) use ``DecimalText``: SQLite has no
real decimal type and SQLAlchemy's ``Numeric`` round-trips through REAL, which is lossy.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import String
from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator


class DecimalText(TypeDecorator[Decimal]):
    """Stores a ``Decimal`` as its exact string form. Rejects floats outright."""

    impl = String(64)
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Dialect) -> str | None:
        if value is None:
            return None
        if isinstance(value, float):
            raise TypeError("Floats are not allowed for exact decimal columns; pass a Decimal or str")
        if isinstance(value, int | str):
            value = Decimal(value)
        if not isinstance(value, Decimal):
            raise TypeError(f"Expected Decimal, got {type(value).__name__}")
        if not value.is_finite():
            raise ValueError("Non-finite decimals are not allowed")
        return format(value, "f")

    def process_result_value(self, value: Any, dialect: Dialect) -> Decimal | None:
        return None if value is None else Decimal(value)


def utcnow() -> datetime:
    """Naive UTC timestamp (SQLite stores no tz); every timestamp column is UTC by convention."""
    return datetime.now(UTC).replace(tzinfo=None)
