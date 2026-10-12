"""Tax documents (Form 16, AIS/TIS, 26AS, certificates, filed ITRs) and manual inputs."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import JSON, BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from taxcopilot.models.base import Base, CreatedAtMixin, str_enum
from taxcopilot.models.enums import TaxDocType


class TaxDocument(CreatedAtMixin, Base):
    __tablename__ = "tax_document"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_file_id: Mapped[int | None] = mapped_column(ForeignKey("source_file.id"))
    doc_type: Mapped[TaxDocType] = mapped_column(str_enum(TaxDocType))
    fy: Mapped[str] = mapped_column(String(7), index=True)
    issuer_name: Mapped[str | None] = mapped_column(String(200))  # employer, bank, insurer
    issuer_tan: Mapped[str | None] = mapped_column(String(10))
    # Structured content, e.g. Form 16 Part B: gross salary, 10(13A), 16(ia), Chapter VI-A claimed.
    details: Mapped[dict[str, Any]] = mapped_column(default=dict)


class TaxDocumentItem(Base):
    """One line of AIS/TIS/26AS/Form 16 Part A: a payer, a section, an amount, and tax deducted."""

    __tablename__ = "tax_document_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    tax_document_id: Mapped[int] = mapped_column(ForeignKey("tax_document.id"), index=True)
    section_code: Mapped[str | None] = mapped_column(String(16))  # "192", "194A", "206C(1G)"
    info_code: Mapped[str | None] = mapped_column(String(32))  # AIS info code, e.g. "SFT-005"
    payer_name: Mapped[str | None] = mapped_column(String(200))
    payer_tan_or_pan: Mapped[str | None] = mapped_column(String(10))
    txn_date: Mapped[date | None]
    quarter: Mapped[str | None] = mapped_column(String(2))
    amount_paise: Mapped[int | None] = mapped_column(BigInteger)
    tds_paise: Mapped[int | None] = mapped_column(BigInteger)
    tcs_paise: Mapped[int | None] = mapped_column(BigInteger)
    derived_amount_paise: Mapped[int | None] = mapped_column(BigInteger)  # TIS "derived value"
    feedback_status: Mapped[str | None] = mapped_column(String(64))
    details: Mapped[dict[str, Any]] = mapped_column(default=dict)
    raw_row_id: Mapped[int | None] = mapped_column(ForeignKey("raw_row.id"))


class ManualInput(CreatedAtMixin, Base):
    """Facts only I can supply: rent paid, landlord PAN, city, parents' age for 80D, etc.

    Keys and value shapes are declared in rules/manual_inputs.yaml. Edits supersede, never overwrite,
    so a computation can always show which version of an input it used.
    """

    __tablename__ = "manual_input"

    id: Mapped[int] = mapped_column(primary_key=True)
    fy: Mapped[str] = mapped_column(String(7), index=True)
    key: Mapped[str] = mapped_column(String(96))
    value: Mapped[Any] = mapped_column(JSON)
    note: Mapped[str | None] = mapped_column(Text)
    superseded_at: Mapped[datetime | None]
