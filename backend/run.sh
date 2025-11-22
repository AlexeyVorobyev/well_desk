#!/usr/bin/env bash
set -euo pipefail

APP_HOST=${APP_HOST:-0.0.0.0}
APP_PORT=${APP_PORT:-8081}

cd "$(dirname "$0")"

if command -v uv >/dev/null 2>&1; then
  uv run uvicorn app.main:app --host "$APP_HOST" --port "$APP_PORT"
else
  uvicorn app.main:app --host "$APP_HOST" --port "$APP_PORT"
fi
