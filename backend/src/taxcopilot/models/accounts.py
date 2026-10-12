from __future__ import annotations

from datetime import date
from typing import Any

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from taxcopilot.models.base import Base, CreatedAtMixin, str_enum
from taxcopilot.models.enums import AccountType, Owner


class Account(CreatedAtMixin, Base):
    """Any place money or securities sit: bank, card, broker ledger, FD, folio, EPF, loan..."""

    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    institution: Mapped[str] = mapped_column(String(100))  # display name, "HDFC Bank"
    institution_code: Mapped[str] = mapped_column(String(32), index=True)  # "hdfc"; parsers match on it
    type: Mapped[AccountType] = mapped_column(str_enum(AccountType))
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    masked_number: Mapped[str | None] = mapped_column(String(8))  # last 4 only, never the full number
    nickname: Mapped[str] = mapped_column(String(100))
    owner: Mapped[Owner] = mapped_column(str_enum(Owner), default=Owner.SELF)
    # FD under the savings account that funded it; sweep FDs; card add-ons.
    parent_account_id: Mapped[int | None] = mapped_column(ForeignKey("account.id"))
    # Non-secret identifiers useful for matching: IFSC, Zerodha client id, folio no., CRN.
    external_ids: Mapped[dict[str, Any]] = mapped_column(default=dict)
    # Type-specific facts, e.g. FD principal/rate/maturity/cumulative, loan sanction amount.
    details: Mapped[dict[str, Any]] = mapped_column(default=dict)
    opened_on: Mapped[date | None]
    closed_on: Mapped[date | None]

    @property
    def is_mine(self) -> bool:
        return self.owner in (Owner.SELF, Owner.JOINT)
