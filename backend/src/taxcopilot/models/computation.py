"""Tax computations as a tree of lines, each with a formula and links back to its sources."""

from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from taxcopilot.models.base import Base, CreatedAtMixin, str_enum
from taxcopilot.models.enums import ComputationStatus, LineSourceKind, Regime


class TaxComputation(CreatedAtMixin, Base):
    __tablename__ = "tax_computation"

    id: Mapped[int] = mapped_column(primary_key=True)
    fy: Mapped[str] = mapped_column(String(7), index=True)
    regime: Mapped[Regime] = mapped_column(str_enum(Regime))
    status: Mapped[ComputationStatus] = mapped_column(str_enum(ComputationStatus))
    is_projection: Mapped[bool] = mapped_column(default=False)
    as_of: Mapped[date]  # ledger cut-off used (YTD for the current year)
    rules_file: Mapped[str] = mapped_column(String(64))  # "FY2025-26.yaml"
    rules_file_sha256: Mapped[str] = mapped_column(String(64))
    rules_file_version: Mapped[int]
    engine_version: Mapped[str] = mapped_column(String(16))
    inputs_hash: Mapped[str] = mapped_column(String(64))  # detects stale computations
    summary: Mapped[dict[str, Any]] = mapped_column(default=dict)
    # Every unverified rule or TAX-VERIFY note the computation touched, surfaced in the UI.
    verification_flags: Mapped[list[Any]] = mapped_column(default=list)


class TaxComputationLine(Base):
    __tablename__ = "tax_computation_line"

    id: Mapped[int] = mapped_column(primary_key=True)
    computation_id: Mapped[int] = mapped_column(ForeignKey("tax_computation.id"), index=True)
    key: Mapped[str] = mapped_column(String(128))  # stable, e.g. "gti.other_sources.sb_interest"
    parent_key: Mapped[str | None] = mapped_column(String(128))
    sort_order: Mapped[int]
    label: Mapped[str] = mapped_column(String(200))
    amount_paise: Mapped[int] = mapped_column(BigInteger)
    formula: Mapped[str | None] = mapped_column(Text)  # human-readable, with values substituted
    rule_refs: Mapped[list[Any]] = mapped_column(default=list)  # rule ids from the YAML file
    section_old: Mapped[str | None] = mapped_column(String(32))  # Income-tax Act, 1961
    section_new: Mapped[str | None] = mapped_column(String(32))  # Income-tax Act, 2025
    flags: Mapped[list[Any]] = mapped_column(default=list)


class TaxLineSource(Base):
    """Edge in the drill-down graph: this line includes `amount_paise` from that source."""

    __tablename__ = "tax_line_source"

    id: Mapped[int] = mapped_column(primary_key=True)
    line_id: Mapped[int] = mapped_column(ForeignKey("tax_computation_line.id"), index=True)
    source_kind: Mapped[LineSourceKind] = mapped_column(str_enum(LineSourceKind))
    source_id: Mapped[int]
    amount_paise: Mapped[int] = mapped_column(BigInteger)
