"""Enumerations shared by the schema.

Stored as plain strings (no CHECK constraints) so adding a value never needs a SQLite table rebuild;
validation happens in the application layer.
"""

from enum import StrEnum


class AccountType(StrEnum):
    SAVINGS = "savings"
    CURRENT = "current"
    CREDIT_CARD = "credit_card"
    DEMAT_LEDGER = "demat_ledger"  # Indian broker: cash ledger + the demat holdings behind it
    BROKER_US = "broker_us"  # foreign broker: USD cash + positions
    FD = "fd"
    RD = "rd"
    MF_FOLIO = "mf_folio"
    EPF = "epf"
    PPF = "ppf"
    NPS = "nps"
    LOAN = "loan"
    WALLET = "wallet"
    OTHER = "other"


class Owner(StrEnum):
    SELF = "self"
    JOINT = "joint"  # treated as "mine" for transfer linking
    OTHER = "other"  # e.g. a family member's account I have statements for; never a self-transfer


class SourceFileStatus(StrEnum):
    UPLOADED = "uploaded"
    NEEDS_PASSWORD = "needs_password"
    NEEDS_PARSER = "needs_parser"  # detection ambiguous: user picks the parser / mapping template
    NEEDS_ACCOUNT = "needs_account"  # parsed hints, waiting for user to confirm the account
    PARSED = "parsed"
    PARSED_WITH_WARNINGS = "parsed_with_warnings"
    FAILED = "failed"


class ParseRunStatus(StrEnum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class TieOutStatus(StrEnum):
    OK = "ok"
    FAILED = "failed"
    NOT_APPLICABLE = "not_applicable"
    UNKNOWN = "unknown"  # file states no opening/closing balance


class RawRowKind(StrEnum):
    TRANSACTION = "transaction"
    OPENING_BALANCE = "opening_balance"
    CLOSING_BALANCE = "closing_balance"
    HEADER = "header"
    SUMMARY = "summary"
    OTHER = "other"


class Channel(StrEnum):
    UPI = "upi"
    NEFT = "neft"
    RTGS = "rtgs"
    IMPS = "imps"
    ACH = "ach"
    NACH = "nach"
    ECS = "ecs"
    CHEQUE = "cheque"
    ATM = "atm"
    POS = "pos"
    CARD = "card"
    NETBANKING = "netbanking"
    STANDING_INSTRUCTION = "standing_instruction"
    INTERNAL = "internal"  # interest, charges, sweeps, TDS posted by the bank itself
    SWIFT = "swift"
    OTHER = "other"
    UNKNOWN = "unknown"


class LinkType(StrEnum):
    SELF_TRANSFER = "self_transfer"
    INVESTMENT_FUNDING = "investment_funding"  # bank -> broker ledger / MF / US broker
    INVESTMENT_PAYOUT = "investment_payout"  # broker / MF redemption -> bank
    LRS_REMITTANCE = "lrs_remittance"  # INR debit <-> USD credit (+ TCS leg)
    CARD_BILL_PAYMENT = "card_bill_payment"
    FD_BOOKING = "fd_booking"
    FD_MATURITY = "fd_maturity"
    FD_PREMATURE_CLOSURE = "fd_premature_closure"
    SWEEP = "sweep"
    REFUND = "refund"
    REVERSAL = "reversal"
    LOAN_EMI = "loan_emi"
    SALARY = "salary"  # salary credit <-> Form 16 / payslip month
    OTHER = "other"


class LinkStatus(StrEnum):
    PROPOSED = "proposed"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"  # remembered, so the matcher never re-proposes the same pair


class Method(StrEnum):
    """How a link or category assignment was decided. Ordered roughly by authority."""

    MANUAL = "manual"
    USER_RULE = "user_rule"
    BUILTIN_RULE = "builtin_rule"
    STRUCTURAL = "structural"  # e.g. it is a confirmed transfer leg; it is on a broker ledger
    AUTO = "auto"  # scored matcher (linking)
    LLM = "llm"
    DEFAULT = "default"


class LegRole(StrEnum):
    SOURCE = "source"
    DESTINATION = "destination"
    FEE = "fee"
    TAX = "tax"  # e.g. TCS collected on an LRS remittance
    ORIGINAL = "original"  # refund/reversal: the debit being undone
    COUNTER = "counter"  # refund/reversal: the credit undoing it


class TaxBucket(StrEnum):
    """Top-level tax bucket. Leaf codes (``tax_code``) come from rules/taxonomy.yaml."""

    INCOME_SALARY = "income_salary"
    INCOME_HOUSE_PROPERTY = "income_house_property"
    INCOME_CAPITAL_GAINS = "income_capital_gains"
    INCOME_BUSINESS = "income_business"
    INCOME_OTHER_SOURCES = "income_other_sources"
    EXEMPT_INCOME = "exempt_income"
    DEDUCTION = "deduction"
    TAX_PAID = "tax_paid"
    TRANSFER = "transfer"
    INVESTMENT = "investment"
    EXPENSE = "expense"
    UNKNOWN = "unknown"


class AssetClass(StrEnum):
    EQUITY_LISTED_IN = "equity_listed_in"
    EQUITY_UNLISTED_IN = "equity_unlisted_in"
    MUTUAL_FUND = "mutual_fund"  # tax treatment derived per FY from scheme facts, not stored here
    ETF_IN = "etf_in"
    FOREIGN_EQUITY = "foreign_equity"
    FOREIGN_ETF = "foreign_etf"
    SGB = "sgb"
    GOLD = "gold"
    BOND = "bond"
    DERIVATIVE = "derivative"
    OTHER = "other"


class Segment(StrEnum):
    EQUITY_DELIVERY = "equity_delivery"
    EQUITY_INTRADAY = "equity_intraday"
    FNO_FUTURES = "fno_futures"
    FNO_OPTIONS = "fno_options"
    MUTUAL_FUND = "mutual_fund"
    FOREIGN = "foreign"
    OTHER = "other"


class InvestmentEventType(StrEnum):
    BUY = "buy"
    SELL = "sell"
    BONUS = "bonus"
    SPLIT = "split"
    MERGER_IN = "merger_in"
    MERGER_OUT = "merger_out"
    DEMERGER = "demerger"
    BUYBACK = "buyback"
    RSU_VEST = "rsu_vest"
    ESPP_PURCHASE = "espp_purchase"
    DIVIDEND_REINVEST = "dividend_reinvest"
    SWITCH_IN = "switch_in"
    SWITCH_OUT = "switch_out"
    TRANSFER_IN = "transfer_in"  # off-market / demat-to-demat
    TRANSFER_OUT = "transfer_out"
    REDEMPTION = "redemption"  # SGB/bond maturity, MF closure


class GainTerm(StrEnum):
    SHORT = "short"
    LONG = "long"


class TaxDocType(StrEnum):
    FORM16_PART_A = "form16_part_a"
    FORM16_PART_B = "form16_part_b"
    PAYSLIP = "payslip"
    AIS = "ais"
    TIS = "tis"
    FORM26AS = "form26as"
    INTEREST_CERTIFICATE = "interest_certificate"
    HOME_LOAN_CERTIFICATE = "home_loan_certificate"
    RENT_RECEIPT = "rent_receipt"
    INSURANCE_PREMIUM = "insurance_premium"
    DONATION_RECEIPT = "donation_receipt"
    FILED_ITR = "filed_itr"  # the JSON/PDF of a return already filed: best source for carried-forward losses


class Regime(StrEnum):
    OLD = "old"
    NEW = "new"


class ComputationStatus(StrEnum):
    DRAFT = "draft"
    FINAL = "final"  # only allowed when the FY has zero UNKNOWN tax buckets


class UserRuleKind(StrEnum):
    CATEGORISE = "categorise"
    LINK = "link"
    ACCOUNT_MATCH = "account_match"  # "files with this header/last-4 belong to account X"
    IGNORE = "ignore"


class LineSourceKind(StrEnum):
    TRANSACTION = "transaction"
    CATEGORY_ASSIGNMENT = "category_assignment"
    DISPOSAL = "disposal"
    TAX_DOCUMENT_ITEM = "tax_document_item"
    MANUAL_INPUT = "manual_input"
    COMPUTATION_LINE = "computation_line"
