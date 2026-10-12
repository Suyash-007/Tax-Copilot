"""Securities: instruments, trade/corporate-action events, FIFO lots and the disposals matched to them.

Lots and disposals are *derived* by the capital-gains engine from events; they are stored so the
Tax page can drill into them, and are rebuilt whenever events or rules change.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import BigInteger, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from taxcopilot.models.base import Base, CreatedAtMixin, str_enum
from taxcopilot.models.enums import AssetClass, GainTerm, InvestmentEventType, Segment


class Instrument(Base):
    __tablename__ = "instrument"

    id: Mapped[int] = mapped_column(primary_key=True)
    isin: Mapped[str | None] = mapped_column(String(12), unique=True)
    symbol: Mapped[str | None] = mapped_column(String(32), index=True)
    exchange: Mapped[str | None] = mapped_column(String(16))  # NSE, BSE, NASDAQ, NYSE
    name: Mapped[str] = mapped_column(String(200))
    asset_class: Mapped[AssetClass] = mapped_column(str_enum(AssetClass))
    country: Mapped[str] = mapped_column(String(2), default="IN")
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    # Mutual funds: raw facts only. The tax class (equity-oriented / specified MF u/s 50AA / other)
    # depends on the FY's rules, so the engine derives it rather than storing it.
    amfi_scheme_code: Mapped[str | None] = mapped_column(String(16))
    mf_facts: Mapped[dict[str, Any]] = mapped_column(default=dict)  # SEBI category, equity %, FoF?
    tax_class_override: Mapped[str | None] = mapped_column(String(32))  # user override, audited
    # Grandfathering u/s 55(2)(ac): highest listed price (shares) or NAV (MF units) on 31-Jan-2018.
    fmv_31jan2018: Mapped[Decimal | None]
    fmv_31jan2018_source: Mapped[str | None] = mapped_column(String(128))


class InvestmentEvent(CreatedAtMixin, Base):
    """A trade or corporate action from a tradebook, CAS, broker statement or vest report."""

    __tablename__ = "investment_event"
    __table_args__ = (
        UniqueConstraint("account_id", "dedupe_key"),
        Index("ix_inv_event_instr_date", "instrument_id", "trade_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instrument.id"))
    event_type: Mapped[InvestmentEventType] = mapped_column(str_enum(InvestmentEventType))
    segment: Mapped[Segment] = mapped_column(str_enum(Segment))
    trade_date: Mapped[date]
    settle_date: Mapped[date | None]
    quantity: Mapped[Decimal]  # always positive; direction comes from event_type
    price: Mapped[Decimal | None]  # per unit, in `currency`
    gross_minor: Mapped[int | None] = mapped_column(BigInteger)
    # brokerage, stt, exchange_txn, sebi, stamp, gst, other: each in minor units
    charges: Mapped[dict[str, Any]] = mapped_column(default=dict)
    net_minor: Mapped[int | None] = mapped_column(BigInteger)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    fx_rate_to_inr: Mapped[Decimal | None]
    fx_rate_source: Mapped[str | None] = mapped_column(String(64))
    # Bonus/split ratios, merger swap ratios, RSU vest FMV, ESPP discount, etc.
    details: Mapped[dict[str, Any]] = mapped_column(default=dict)
    external_ref: Mapped[str | None] = mapped_column(String(64))  # trade id / order id / CAS txn id
    dedupe_key: Mapped[str] = mapped_column(String(64))
    raw_row_id: Mapped[int | None] = mapped_column(ForeignKey("raw_row.id"))
    source_file_id: Mapped[int | None] = mapped_column(ForeignKey("source_file.id"))
    cash_transaction_id: Mapped[int | None] = mapped_column(ForeignKey("txn.id"))  # its money leg


class Lot(Base):
    __tablename__ = "lot"
    __table_args__ = (Index("ix_lot_fifo", "account_id", "instrument_id", "acquired_on"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instrument.id"))
    acquired_on: Mapped[date]
    acquisition_event_id: Mapped[int | None] = mapped_column(ForeignKey("investment_event.id"))
    quantity_original: Mapped[Decimal]
    quantity_open: Mapped[Decimal]
    cost_paise: Mapped[int] = mapped_column(BigInteger)  # incl. acquisition expenses
    cost_foreign_minor: Mapped[int | None] = mapped_column(BigInteger)
    fx_rate_at_acquisition: Mapped[Decimal | None]
    origin: Mapped[str] = mapped_column(String(32))  # "trade" | "holdings_import" | "manual" | "bonus"


class Disposal(Base):
    __tablename__ = "disposal"
    __table_args__ = (Index("ix_disposal_fy", "fy", "rule_bucket"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lot.id"), index=True)
    sell_event_id: Mapped[int] = mapped_column(ForeignKey("investment_event.id"), index=True)
    sell_date: Mapped[date]
    fy: Mapped[str] = mapped_column(String(7))  # "2024-25"
    quantity: Mapped[Decimal]
    proceeds_paise: Mapped[int] = mapped_column(BigInteger)
    expenses_paise: Mapped[int] = mapped_column(BigInteger)  # transfer expenses (not STT)
    cost_paise: Mapped[int] = mapped_column(BigInteger)  # actual allocated cost
    cost_for_tax_paise: Mapped[int] = mapped_column(BigInteger)  # after grandfathering/indexation
    holding_days: Mapped[int]
    term: Mapped[GainTerm] = mapped_column(str_enum(GainTerm))
    gain_paise: Mapped[int] = mapped_column(BigInteger)
    # Rule-file bucket id, e.g. "cg.equity_112a.post_2024_07_23", "cg.specified_mf_50aa".
    rule_bucket: Mapped[str] = mapped_column(String(96))
    details: Mapped[dict[str, Any]] = mapped_column(default=dict)  # FX conversions, FMV used, why
    engine_version: Mapped[str] = mapped_column(String(16))
