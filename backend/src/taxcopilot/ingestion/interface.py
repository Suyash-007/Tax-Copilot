"""Parser plugin contract.

A parser is a pure function of the file: it never touches the database, never guesses the account
id, and never decides duplicates. It returns what the file says, with every record pointing at the
raw row it came from. The ingestion service then resolves the account (with the user's
confirmation), deduplicates, persists, and runs the balance tie-out.

Lifecycle (see docs/PHASE0_PLAN.md §5):
    upload -> sniff format -> (password prompt -> unlock in memory) -> detect (all parsers)
    -> pick parser (auto if one clear winner, else ask) -> parse -> validate -> confirm account
    -> dedupe + persist -> tie-out -> coverage update
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from enum import StrEnum
from typing import Any, ClassVar, Protocol

from pydantic import BaseModel, Field

from taxcopilot.models.enums import AccountType, InvestmentEventType, RawRowKind, Segment


class FileFormat(StrEnum):
    PDF = "pdf"
    XLSX = "xlsx"
    XLS = "xls"  # legacy BIFF; several banks' "XLS" downloads are really HTML or TSV: sniffed, not trusted
    CSV = "csv"
    HTML = "html"
    JSON = "json"
    UNKNOWN = "unknown"


class DocumentKind(StrEnum):
    BANK_STATEMENT = "bank_statement"
    CARD_STATEMENT = "card_statement"
    BROKER_LEDGER = "broker_ledger"
    TRADEBOOK = "tradebook"
    TAX_PNL = "tax_pnl"
    HOLDINGS = "holdings"
    DIVIDEND_STATEMENT = "dividend_statement"
    MF_CAS = "mf_cas"
    FD_CERTIFICATE = "fd_certificate"
    FOREIGN_BROKER_STATEMENT = "foreign_broker_statement"
    FORM16 = "form16"
    PAYSLIP = "payslip"
    AIS = "ais"
    TIS = "tis"
    FORM26AS = "form26as"
    OTHER = "other"


class FileProbe(Protocol):
    """Cheap, cached views of one uploaded file, shared by every parser's ``detect``.

    Implementations hold decrypted bytes in memory only; the password is never stored or logged.
    """

    filename: str
    sha256: str
    format: FileFormat
    is_encrypted: bool  # True while still locked; detect() sees only filename/format then

    def data(self) -> bytes: ...

    def text_head(self, pages: int = 1) -> str:
        """Extracted text of the first ``pages`` PDF pages ('' for non-PDF)."""
        ...

    def table_head(self, rows: int = 40, sheet: str | None = None) -> list[list[str]]:
        """First ``rows`` rows of a tabular file as strings ([] for PDF)."""
        ...

    def sheet_names(self) -> list[str]: ...


# ---------------------------------------------------------------------------------------------
# Detection


class AccountHint(BaseModel):
    """What the file says about whose account it is. Matched against Account rows; never trusted blindly."""

    institution_code: str | None = None
    account_type: AccountType | None = None
    masked_number: str | None = None  # last 4
    holder_name: str | None = None
    currency: str | None = None
    external_ids: dict[str, str] = Field(default_factory=dict)  # IFSC, client id, folio...


class Detection(BaseModel):
    confidence: float = Field(ge=0.0, le=1.0)
    reasons: list[str] = Field(default_factory=list)  # shown in the upload UI
    needs_password: bool = False
    account_hint: AccountHint | None = None
    period_start: date | None = None
    period_end: date | None = None


# ---------------------------------------------------------------------------------------------
# Parse output. Amounts are integer minor units of the statement currency; quantities are Decimal.


class RawRowOut(BaseModel):
    page: int | None = None
    sheet: str | None = None
    row_index: int
    text: str
    cells: list[str] | None = None
    bbox: tuple[float, float, float, float] | None = None
    kind: RawRowKind


class StatementMeta(BaseModel):
    account: AccountHint
    period_start: date | None = None
    period_end: date | None = None
    opening_balance_minor: int | None = None
    closing_balance_minor: int | None = None
    stated_debits_minor: int | None = None
    stated_credits_minor: int | None = None
    stated_txn_count: int | None = None


class CashTxnRecord(BaseModel):
    raw_row: int  # index into ParseResult.raw_rows
    txn_date: date
    value_date: date | None = None
    amount_minor: int  # signed: credit +, debit -
    currency: str = "INR"
    narration: str
    running_balance_minor: int | None = None
    refs: dict[str, str] = Field(default_factory=dict)  # utr / upi / imps / cheque, if the file has columns


class InvestmentEventRecord(BaseModel):
    raw_row: int
    event_type: InvestmentEventType
    segment: Segment
    trade_date: date
    settle_date: date | None = None
    isin: str | None = None
    symbol: str | None = None
    instrument_name: str | None = None
    quantity: Decimal
    price: Decimal | None = None
    gross_minor: int | None = None
    charges_minor: dict[str, int] = Field(default_factory=dict)
    currency: str = "INR"
    external_ref: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class HoldingRecord(BaseModel):
    """A point-in-time position (holdings file, CAS closing balance) used to seed or verify lots."""

    raw_row: int
    as_of: date
    isin: str | None = None
    symbol: str | None = None
    instrument_name: str | None = None
    quantity: Decimal
    avg_cost: Decimal | None = None
    currency: str = "INR"


class TaxItemRecord(BaseModel):
    raw_row: int
    section_code: str | None = None
    info_code: str | None = None
    payer_name: str | None = None
    payer_tan_or_pan: str | None = None
    txn_date: date | None = None
    amount_minor: int | None = None
    tds_minor: int | None = None
    tcs_minor: int | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class ParseResult(BaseModel):
    document_kind: DocumentKind
    statement: StatementMeta | None = None
    raw_rows: list[RawRowOut]
    cash_txns: list[CashTxnRecord] = Field(default_factory=list)
    investment_events: list[InvestmentEventRecord] = Field(default_factory=list)
    holdings: list[HoldingRecord] = Field(default_factory=list)
    tax_items: list[TaxItemRecord] = Field(default_factory=list)
    document_details: dict[str, Any] = Field(default_factory=dict)  # e.g. Form 16 Part B fields
    warnings: list[str] = Field(default_factory=list)


class ParseContext(BaseModel):
    """Inputs a parser may need beyond the file itself."""

    column_mapping: dict[str, Any] | None = None  # generic mapper template
    default_currency: str = "INR"
    year_hint: int | None = None  # for layouts that print "12 Mar" without a year


# ---------------------------------------------------------------------------------------------


class Parser(ABC):
    """Base class for every file parser.

    Contract for implementers:
    * ``id`` is stable forever ("hdfc.bank.pdf"); ``version`` is bumped on any change that alters
      output, which lets the app offer a re-parse and diff.
    * ``detect`` must be cheap (use the probe's cached heads) and must not raise; return 0.0 if unsure.
    * ``parse`` must emit a RawRowOut for every line it read, including headers and summary rows it
      skipped, so the audit trail is complete.
    * Every parser ships with an anonymised fixture and an ``expected.yaml`` (row count, opening,
      closing, total debits/credits) under tests/fixtures/<parser id>/.
    """

    id: ClassVar[str]
    version: ClassVar[str]
    document_kind: ClassVar[DocumentKind]
    institution_code: ClassVar[str | None] = None
    formats: ClassVar[frozenset[FileFormat]]

    @classmethod
    @abstractmethod
    def detect(cls, probe: FileProbe) -> Detection: ...

    @abstractmethod
    def parse(self, probe: FileProbe, ctx: ParseContext) -> ParseResult: ...
