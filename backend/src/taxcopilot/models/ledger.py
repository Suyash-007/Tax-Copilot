"""The normalised cash ledger, cross-account links and category assignments."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import BigInteger, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from taxcopilot.models.base import Base, CreatedAtMixin, str_enum
from taxcopilot.models.enums import Channel, LegRole, LinkStatus, LinkType, Method, TaxBucket


class Transaction(CreatedAtMixin, Base):
    """One cash movement in one account.

    Sign convention: from the account holder's point of view. Credit (money in) is positive,
    debit (money out) is negative. On a credit card a purchase is negative and a payment positive.
    """

    __tablename__ = "txn"
    __table_args__ = (
        # Idempotent ingestion. See docs/PHASE0_PLAN.md §4.3 for how the key and ordinal are built.
        UniqueConstraint("account_id", "dedupe_key", "dedupe_ordinal"),
        Index("ix_txn_account_date", "account_id", "txn_date"),
        Index("ix_txn_date_amount", "txn_date", "amount_minor"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    txn_date: Mapped[date]
    value_date: Mapped[date | None]
    amount_minor: Mapped[int] = mapped_column(BigInteger)  # signed, in `currency` minor units
    currency: Mapped[str] = mapped_column(String(3))
    # For non-INR rows: the rate used and where it came from (e.g. "sbi_ttbr:2025-06-30").
    fx_rate_to_inr: Mapped[Decimal | None]
    fx_rate_source: Mapped[str | None] = mapped_column(String(64))
    amount_inr_paise: Mapped[int | None] = mapped_column(BigInteger)  # == amount_minor for INR

    narration_raw: Mapped[str] = mapped_column(Text)
    narration_clean: Mapped[str] = mapped_column(Text)
    counterparty: Mapped[str | None] = mapped_column(String(200))
    counterparty_account_hint: Mapped[str | None] = mapped_column(String(8))  # last-4 seen in narration
    channel: Mapped[Channel] = mapped_column(str_enum(Channel), default=Channel.UNKNOWN)
    ref_upi: Mapped[str | None] = mapped_column(String(64), index=True)
    ref_utr: Mapped[str | None] = mapped_column(String(64), index=True)
    ref_imps: Mapped[str | None] = mapped_column(String(64))
    ref_cheque: Mapped[str | None] = mapped_column(String(32))
    ref_other: Mapped[dict[str, Any]] = mapped_column(default=dict)
    running_balance_minor: Mapped[int | None] = mapped_column(BigInteger)

    primary_raw_row_id: Mapped[int] = mapped_column(ForeignKey("raw_row.id"))
    first_source_file_id: Mapped[int] = mapped_column(ForeignKey("source_file.id"))

    dedupe_key: Mapped[str] = mapped_column(String(64))
    dedupe_ordinal: Mapped[int] = mapped_column(default=0)

    # Excluded rows stay in the ledger (for audit) but are ignored by linking and tax.
    is_excluded: Mapped[bool] = mapped_column(default=False)
    exclusion_reason: Mapped[str | None] = mapped_column(String(200))


class TransactionEvidence(Base):
    """Every raw row that evidences a transaction. Overlapping statements add evidence, not rows."""

    __tablename__ = "txn_evidence"

    transaction_id: Mapped[int] = mapped_column(ForeignKey("txn.id"), primary_key=True)
    raw_row_id: Mapped[int] = mapped_column(ForeignKey("raw_row.id"), primary_key=True)
    source_file_id: Mapped[int] = mapped_column(ForeignKey("source_file.id"), index=True)
    match_basis: Mapped[str] = mapped_column(String(32))  # "new" | "balance_key" | "narration_key"


class Link(CreatedAtMixin, Base):
    """Groups 2+ transactions that are one economic event."""

    __tablename__ = "link"

    id: Mapped[int] = mapped_column(primary_key=True)
    link_type: Mapped[LinkType] = mapped_column(str_enum(LinkType))
    status: Mapped[LinkStatus] = mapped_column(str_enum(LinkStatus), index=True)
    method: Mapped[Method] = mapped_column(str_enum(Method))
    confidence: Mapped[float]  # 0..1; a score, not money
    score_breakdown: Mapped[dict[str, Any]] = mapped_column(default=dict)  # why, for the Review Queue
    user_rule_id: Mapped[int | None] = mapped_column(ForeignKey("user_rule.id"))
    decided_at: Mapped[datetime | None]
    note: Mapped[str | None] = mapped_column(Text)


class LinkLeg(Base):
    __tablename__ = "link_leg"
    __table_args__ = (UniqueConstraint("link_id", "transaction_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    link_id: Mapped[int] = mapped_column(ForeignKey("link.id"), index=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("txn.id"), index=True)
    role: Mapped[LegRole] = mapped_column(str_enum(LegRole))
    # One-to-many: how much of this leg is allocated to this link (null = whole amount).
    allocated_minor: Mapped[int | None] = mapped_column(BigInteger)


class CategoryAssignment(CreatedAtMixin, Base):
    """Life category + tax bucket for a transaction, or for a split of it.

    Invariant: for each transaction, the current (``superseded_at IS NULL``) assignments' amounts
    sum to the transaction amount. Most transactions have a single split; salary credits (net of
    deductions), EMIs (principal + interest) and foreign dividends (gross + withholding) have several.
    History is kept: a correction supersedes rather than overwrites.
    """

    __tablename__ = "category_assignment"
    __table_args__ = (Index("ix_category_current", "transaction_id", "superseded_at"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("txn.id"))
    split_index: Mapped[int] = mapped_column(default=0)
    amount_minor: Mapped[int] = mapped_column(BigInteger)
    life_category: Mapped[str] = mapped_column(String(64))
    life_subcategory: Mapped[str | None] = mapped_column(String(64))
    tax_bucket: Mapped[TaxBucket] = mapped_column(str_enum(TaxBucket), index=True)
    tax_code: Mapped[str | None] = mapped_column(String(96))  # leaf from rules/taxonomy.yaml
    confidence: Mapped[float]
    method: Mapped[Method] = mapped_column(str_enum(Method))
    user_rule_id: Mapped[int | None] = mapped_column(ForeignKey("user_rule.id"))
    builtin_rule_id: Mapped[str | None] = mapped_column(String(96))
    llm_call_id: Mapped[int | None] = mapped_column(ForeignKey("llm_call_log.id"))
    explanation: Mapped[str | None] = mapped_column(Text)
    superseded_at: Mapped[datetime | None]
