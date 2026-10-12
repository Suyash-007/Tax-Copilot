from typing import ClassVar

from taxcopilot.ingestion.interface import (
    Detection,
    DocumentKind,
    FileFormat,
    FileProbe,
    ParseContext,
    Parser,
    ParseResult,
)
from taxcopilot.ingestion.registry import auto_select, rank


class FakeProbe:
    filename = "statement.pdf"
    sha256 = "0" * 64
    format = FileFormat.PDF
    is_encrypted = False

    def data(self) -> bytes:
        return b""

    def text_head(self, pages: int = 1) -> str:
        return "HDFC BANK Statement of account"

    def table_head(self, rows: int = 40, sheet: str | None = None) -> list[list[str]]:
        return []

    def sheet_names(self) -> list[str]:
        return []


def make_parser(pid: str, conf: float, formats: frozenset[FileFormat]) -> type[Parser]:
    class P(Parser):
        id = pid
        version = "0.0.0"
        document_kind = DocumentKind.BANK_STATEMENT
        formats: ClassVar[frozenset[FileFormat]] = frozenset()

        @classmethod
        def detect(cls, probe: FileProbe) -> Detection:
            return Detection(confidence=conf)

        def parse(self, probe: FileProbe, ctx: ParseContext) -> ParseResult:
            raise NotImplementedError

    P.formats = formats
    return P


class Exploding(Parser):
    id = "exploding"
    version = "0.0.0"
    document_kind = DocumentKind.OTHER
    formats = frozenset({FileFormat.PDF})

    @classmethod
    def detect(cls, probe: FileProbe) -> Detection:
        raise RuntimeError("boom")

    def parse(self, probe: FileProbe, ctx: ParseContext) -> ParseResult:
        raise NotImplementedError


PDF = frozenset({FileFormat.PDF})


def test_rank_skips_wrong_format_and_survives_bad_detector() -> None:
    parsers = [
        make_parser("a", 0.9, PDF),
        make_parser("csv_only", 1.0, frozenset({FileFormat.CSV})),
        Exploding,
    ]
    ranked = rank(FakeProbe(), parsers)
    assert [c.parser.id for c in ranked] == ["a", "exploding"]
    assert ranked[1].detection.confidence == 0.0


def test_auto_select_needs_confidence_and_margin() -> None:
    clear = rank(FakeProbe(), [make_parser("a", 0.95, PDF), make_parser("b", 0.3, PDF)])
    close = rank(FakeProbe(), [make_parser("a", 0.95, PDF), make_parser("b", 0.85, PDF)])
    weak = rank(FakeProbe(), [make_parser("a", 0.6, PDF)])
    assert auto_select(clear) is not None and auto_select(clear).parser.id == "a"  # type: ignore[union-attr]
    assert auto_select(close) is None
    assert auto_select(weak) is None
