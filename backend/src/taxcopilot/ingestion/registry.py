"""Parser registry and detection ranking."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from taxcopilot.ingestion.interface import Detection, FileProbe, Parser

log = logging.getLogger(__name__)

_REGISTRY: dict[str, type[Parser]] = {}

# A parser is auto-selected only if it is confident and clearly ahead of the runner-up;
# otherwise the file goes to NEEDS_PARSER and the user picks.
AUTO_SELECT_MIN_CONFIDENCE = 0.8
AUTO_SELECT_MIN_MARGIN = 0.2


def register(cls: type[Parser]) -> type[Parser]:
    if cls.id in _REGISTRY and _REGISTRY[cls.id] is not cls:
        raise ValueError(f"Duplicate parser id: {cls.id}")
    _REGISTRY[cls.id] = cls
    return cls


def all_parsers() -> list[type[Parser]]:
    return list(_REGISTRY.values())


def get_parser(parser_id: str) -> type[Parser]:
    return _REGISTRY[parser_id]


@dataclass(frozen=True)
class Candidate:
    parser: type[Parser]
    detection: Detection


def rank(probe: FileProbe, parsers: list[type[Parser]] | None = None) -> list[Candidate]:
    """Run every applicable detector; a detector that raises is logged and scored 0."""
    out: list[Candidate] = []
    for p in parsers if parsers is not None else all_parsers():
        if probe.format not in p.formats:
            continue
        try:
            det = p.detect(probe)
        except Exception as exc:  # one bad detector must not block an upload
            log.warning("detector %s failed: %s", p.id, type(exc).__name__)
            det = Detection(confidence=0.0, reasons=[f"detector error: {type(exc).__name__}"])
        out.append(Candidate(p, det))
    return sorted(out, key=lambda c: c.detection.confidence, reverse=True)


def auto_select(candidates: list[Candidate]) -> Candidate | None:
    if not candidates:
        return None
    top = candidates[0].detection.confidence
    runner_up = candidates[1].detection.confidence if len(candidates) > 1 else 0.0
    if top >= AUTO_SELECT_MIN_CONFIDENCE and top - runner_up >= AUTO_SELECT_MIN_MARGIN:
        return candidates[0]
    return None
