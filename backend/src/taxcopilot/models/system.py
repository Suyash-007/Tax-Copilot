"""App settings, the LLM call log, and reference FX rates."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from taxcopilot.models.base import Base, CreatedAtMixin


class AppSetting(Base):
    __tablename__ = "app_setting"

    key: Mapped[str] = mapped_column(String(96), primary_key=True)
    value: Mapped[Any] = mapped_column(JSON)


class LlmCallLog(CreatedAtMixin, Base):
    """Every optional LLM call, with the exact text that left the machine and what came back."""

    __tablename__ = "llm_call_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str] = mapped_column(String(32))
    model: Mapped[str] = mapped_column(String(64))
    purpose: Mapped[str] = mapped_column(String(64))  # "categorise" | "link_hint" | ...
    request_text: Mapped[str] = mapped_column(Text)
    response_text: Mapped[str | None] = mapped_column(Text)
    transaction_ids: Mapped[list[Any]] = mapped_column(default=list)
    error: Mapped[str | None] = mapped_column(Text)


class FxRate(Base):
    """Public reference rates (e.g. SBI TT buying), imported from a file. Not user data."""

    __tablename__ = "fx_rate"
    __table_args__ = (UniqueConstraint("currency", "rate_date", "rate_type"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    currency: Mapped[str] = mapped_column(String(3))
    rate_date: Mapped[date]
    rate_type: Mapped[str] = mapped_column(String(16))  # "sbi_ttbr" | "sbi_ttsr" | "rbi_ref"
    rate: Mapped[Decimal]  # INR per 1 unit of currency
    source: Mapped[str] = mapped_column(String(200))
    details: Mapped[dict[str, Any]] = mapped_column(default=dict)
