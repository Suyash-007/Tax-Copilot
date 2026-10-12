# Working conventions

- Work in phases (docs/PHASE0_PLAN.md §9). Before each phase, post a short plan and the files to
  touch; at the end, demo, list open questions, and stop for a go-ahead.
- Money is integer minor units (`*_paise` = INR, `*_minor` = row currency). Quantities, prices and
  FX rates are `Decimal` via `DecimalText`. Never floats.
- Tax rules live only in `rules/*.yaml`. No slab, limit, rate or date in code. A missing rule is an
  error, not a default.
- Any ambiguous tax point: add a `TAX_QUESTIONS.md` entry and mark the code `# TAX-VERIFY: TQ-nnn`.
- Parsers are pure (no DB). Each ships an anonymised fixture plus `expected.yaml` (tie-out).
- Never commit real statements. `.gitignore` blocks pdf/xls/xlsx/csv outside `backend/tests/fixtures/`.
- Privacy: bind to 127.0.0.1 only, no telemetry (NEXT_TELEMETRY_DISABLED=1), no external requests
  with user data, never log or store passwords.
- Schema change → `make db-revision m="..."`. `tests/test_schema.py` fails if models and
  migrations drift apart.
- `make lint && make test` before every commit.
