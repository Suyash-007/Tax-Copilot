.PHONY: setup dev test lint fmt build db-upgrade db-revision

export NEXT_TELEMETRY_DISABLED := 1

setup:            ## install backend (uv) and frontend (pnpm) dependencies
	cd backend && uv sync
	cd frontend && pnpm install

dev:              ## run engine + UI on 127.0.0.1 (migrates the DB first)
	./scripts/dev.sh

test:             ## backend tests (Playwright smoke test arrives in Phase 8)
	cd backend && uv run pytest

lint:             ## ruff + mypy + eslint + tsc
	cd backend && uv run ruff check . && uv run ruff format --check . && uv run mypy
	cd frontend && pnpm lint && pnpm exec tsc --noEmit

fmt:
	cd backend && uv run ruff format . && uv run ruff check --fix .

build:
	cd frontend && pnpm build

db-upgrade:
	cd backend && uv run alembic upgrade head

db-revision:      ## usage: make db-revision m="add foo"
	cd backend && uv run alembic revision --autogenerate -m "$(m)"
