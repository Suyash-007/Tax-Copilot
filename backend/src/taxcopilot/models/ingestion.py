"""File registry and the audit trail of raw rows. Raw rows are never deleted."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import BigInteger, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from taxcopilot.db_types import utcnow
from taxcopilot.models.base import Base, CreatedAtMixin, str_enum
from taxcopilot.models.enums import ParseRunStatus, RawRowKind, SourceFileStatus, TieOutStatus


class SourceFile(Base):
    __tablename__ = "source_file"

    id: Mapped[int] = mapped_column(primary_key=True)
    sha256: Mapped[str] = mapped_column(String(64), unique=True)  # same bytes twice -> same row
    filename: Mapped[str] = mapped_column(String(255))
    size_bytes: Mapped[int] = mapped_column(BigInteger)
    format: Mapped[str] = mapped_column(String(16))  # sniffed from magic bytes, not the extension
    stored_path: Mapped[str] = mapped_column(String(512))  # copy under data/uploads/<sha256>.<ext>
    was_encrypted: Mapped[bool] = mapped_column(default=False)  # password itself is never stored
    page_count: Mapped[int | None]
    uploaded_at: Mapped[datetime] = mapped_column(default=utcnow)
    status: Mapped[SourceFileStatus] = mapped_column(
        str_enum(SourceFileStatus), default=SourceFileStatus.UPLOADED
    )

    # Detection: ranked candidates with reasons, so the UI can show why a parser was chosen.
    detection_candidates: Mapped[list[Any]] = mapped_column(default=list)
    current_parse_run_id: Mapped[int | None] = mapped_column(ForeignKey("parse_run.id", use_alter=True))

    account_id: Mapped[int | None] = mapped_column(ForeignKey("account.id"), index=True)
    period_start: Mapped[date | None]
    period_end: Mapped[date | None]

    # What the file itself claims (summary block), in the account's minor units.
    stated_opening_minor: Mapped[int | None] = mapped_column(BigInteger)
    stated_closing_minor: Mapped[int | None] = mapped_column(BigInteger)
    stated_debits_minor: Mapped[int | None] = mapped_column(BigInteger)
    stated_credits_minor: Mapped[int | None] = mapped_column(BigInteger)
    stated_txn_count: Mapped[int | None]

    tieout_status: Mapped[TieOutStatus] = mapped_column(str_enum(TieOutStatus), default=TieOutStatus.UNKNOWN)
    tieout_details: Mapped[dict[str, Any]] = mapped_column(default=dict)


class ParseRun(CreatedAtMixin, Base):
    """One execution of one parser version over one file. Re-parsing after a parser upgrade adds a run."""

    __tablename__ = "parse_run"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_file_id: Mapped[int] = mapped_column(ForeignKey("source_file.id"), index=True)
    parser_id: Mapped[str] = mapped_column(String(64))
    parser_version: Mapped[str] = mapped_column(String(16))
    detection_confidence: Mapped[float | None]
    status: Mapped[ParseRunStatus] = mapped_column(str_enum(ParseRunStatus))
    finished_at: Mapped[datetime | None]
    stats: Mapped[dict[str, Any]] = mapped_column(default=dict)  # rows, new txns, merged dupes...
    warnings: Mapped[list[Any]] = mapped_column(default=list)
    errors: Mapped[list[Any]] = mapped_column(default=list)


class RawRow(Base):
    """A line as it appeared in the source, kept forever so every number traces back to text."""

    __tablename__ = "raw_row"
    __table_args__ = (Index("ix_raw_row_file_pos", "source_file_id", "page", "row_index"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    source_file_id: Mapped[int] = mapped_column(ForeignKey("source_file.id"))
    parse_run_id: Mapped[int] = mapped_column(ForeignKey("parse_run.id"), index=True)
    page: Mapped[int | None]  # 1-based, PDFs
    sheet: Mapped[str | None] = mapped_column(String(64))  # XLSX
    row_index: Mapped[int]  # 0-based within page/sheet/file
    raw_text: Mapped[str] = mapped_column(Text)
    cells: Mapped[list[Any] | None]  # cell strings as extracted
    bbox: Mapped[list[Any] | None]  # [x0, top, x1, bottom] in PDF points, for highlight-in-source
    kind: Mapped[RawRowKind] = mapped_column(str_enum(RawRowKind))
