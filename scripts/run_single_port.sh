#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Ensure Reflex can spawn granian in prod/single-port mode.
export PATH="$(pwd)/.venv/bin:$PATH"
export REFLEX_DIR="${REFLEX_DIR:-$(pwd)/.reflex}"

exec .venv/bin/reflex run \
  --env prod \
  --single-port \
  --frontend-port "${AMM_WEB_PORT:-3000}" \
  --backend-host "${AMM_WEB_HOST:-127.0.0.1}"
