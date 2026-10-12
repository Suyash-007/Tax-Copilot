#!/usr/bin/env bash
# Runs the Python engine and the web UI together, both bound to 127.0.0.1. Ctrl-C stops both.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export NEXT_TELEMETRY_DISABLED=1

(cd "$ROOT/backend" && uv run alembic upgrade head)

trap 'kill $(jobs -p) 2>/dev/null || true' EXIT INT TERM
(cd "$ROOT/backend" && uv run uvicorn taxcopilot.main:app --host 127.0.0.1 --port 8000 --reload --reload-dir src) &
(cd "$ROOT/frontend" && pnpm dev --hostname 127.0.0.1 --port 3000) &
echo "Tax Copilot: http://127.0.0.1:3000  (engine: http://127.0.0.1:8000/api/docs)"
wait
