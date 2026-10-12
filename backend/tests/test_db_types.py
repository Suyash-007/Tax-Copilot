from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import Session

from taxcopilot.models import Base, FxRate


@pytest.fixture
def session() -> Session:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    return Session(engine)


def test_decimal_round_trips_exactly(session: Session) -> None:
    rate = Decimal("83.1234567890123456789")
    session.add(
        FxRate(
            currency="USD",
            rate_date=date(2025, 6, 30),
            rate_type="sbi_ttbr",
            rate=rate,
            source="fixture",
        )
    )
    session.commit()
    assert session.scalars(select(FxRate.rate)).one() == rate


def test_float_is_rejected(session: Session) -> None:
    session.add(
        FxRate(
            currency="USD",
            rate_date=date(2025, 6, 30),
            rate_type="sbi_ttbr",
            rate=83.12,
            source="fixture",
        )
    )  # type: ignore[arg-type]
    with pytest.raises(StatementError, match="Floats are not allowed"):
        session.commit()
