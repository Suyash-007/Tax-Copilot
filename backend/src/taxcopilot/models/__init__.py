"""All ORM models. Importing this package registers every table on ``Base.metadata``."""

from taxcopilot.models.accounts import Account
from taxcopilot.models.base import Base
from taxcopilot.models.computation import TaxComputation, TaxComputationLine, TaxLineSource
from taxcopilot.models.ingestion import ParseRun, RawRow, SourceFile
from taxcopilot.models.investments import Disposal, Instrument, InvestmentEvent, Lot
from taxcopilot.models.ledger import (
    CategoryAssignment,
    Link,
    LinkLeg,
    Transaction,
    TransactionEvidence,
)
from taxcopilot.models.rules import ColumnMappingTemplate, UserRule
from taxcopilot.models.system import AppSetting, FxRate, LlmCallLog
from taxcopilot.models.taxdocs import ManualInput, TaxDocument, TaxDocumentItem

__all__ = [
    "Account",
    "AppSetting",
    "Base",
    "CategoryAssignment",
    "ColumnMappingTemplate",
    "Disposal",
    "FxRate",
    "Instrument",
    "InvestmentEvent",
    "Link",
    "LinkLeg",
    "LlmCallLog",
    "Lot",
    "ManualInput",
    "ParseRun",
    "RawRow",
    "SourceFile",
    "TaxComputation",
    "TaxComputationLine",
    "TaxDocument",
    "TaxDocumentItem",
    "TaxLineSource",
    "Transaction",
    "TransactionEvidence",
    "UserRule",
]
