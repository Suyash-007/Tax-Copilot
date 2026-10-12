"""User-created rules (from corrections) and saved column mappings for the generic bank mapper.

Statutory tax rules are NOT here: they live in versioned YAML files under /rules.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from taxcopilot.models.base import Base, CreatedAtMixin, str_enum
from taxcopilot.models.enums import AccountType, UserRuleKind


class UserRule(CreatedAtMixin, Base):
    """e.g. "narration contains ACH/ZERODHA -> transfer to Zerodha", re-applied retroactively.

    ``conditions``: narration contains/regex, account ids, direction, amount range, channel, counterparty.
    ``action``: set category/tax bucket, or link to account X with link type Y.
    """

    __tablename__ = "user_rule"

    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[UserRuleKind] = mapped_column(str_enum(UserRuleKind))
    name: Mapped[str] = mapped_column(String(200))
    priority: Mapped[int] = mapped_column(default=100)  # lower runs first
    enabled: Mapped[bool] = mapped_column(default=True)
    conditions: Mapped[dict[str, Any]]
    action: Mapped[dict[str, Any]]
    created_from_transaction_id: Mapped[int | None] = mapped_column(ForeignKey("txn.id"))
    hit_count: Mapped[int] = mapped_column(default=0)
    last_applied_at: Mapped[datetime | None]


class ColumnMappingTemplate(CreatedAtMixin, Base):
    """Generic CSV/XLS mapper: map Date/Narration/Debit/Credit/Balance once, reuse by header signature."""

    __tablename__ = "column_mapping_template"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    institution_code: Mapped[str] = mapped_column(String(32))
    account_type: Mapped[AccountType] = mapped_column(str_enum(AccountType))
    header_signature: Mapped[str] = mapped_column(String(64), index=True)  # hash of normalised header
    # columns, date format, amount style (debit/credit cols | signed | Dr/Cr flag), rows to skip
    mapping: Mapped[dict[str, Any]]
