# Tax Copilot

A local-first web app for one resident Indian salaried individual. You upload raw files (bank
statements, Zerodha reports, MF CAS, FD certificates, US broker statements, Form 16, AIS/TIS/26AS).
It rebuilds a single ledger across accounts, links transfers between your own accounts, categorises
everything into tax buckets, computes tax under both regimes for FY 2022-23 to tax year 2026-27, and
explains what goes where in the ITR.

**Decision support, not professional tax advice.** It prepares and explains; you file on the
income-tax portal yourself. All data stays on your machine: SQLite under `data/`, no telemetry, no
external APIs for your data.

## Run

Needs Python ≥ 3.12 with [uv](https://docs.astral.sh/uv/), and Node ≥ 20 with pnpm.

```sh
make setup   # install dependencies
make dev     # http://127.0.0.1:3000  (engine API docs at http://127.0.0.1:8000/api/docs)
make test    # backend tests
make lint    # ruff, mypy --strict, eslint, tsc
```

## Docs

- [`docs/PHASE0_PLAN.md`](docs/PHASE0_PLAN.md): architecture, schema, parser interface, phase plan, open questions
- [`rules/README.md`](rules/README.md): how statutory rules are stored as versioned data
- [`TAX_QUESTIONS.md`](TAX_QUESTIONS.md): every tax edge case, with best reading and sources

## Status

Phase 0 (plan + scaffold). Nothing parses or computes yet.
