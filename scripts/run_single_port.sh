#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Ensure Reflex can spawn granian in prod/single-port mode.
export PATH="$(pwd)/.venv/bin:$PATH"
export REFLEX_DIR="${REFLEX_DIR:-$(pwd)/.reflex}"
export REFLEX_USE_NPM="${REFLEX_USE_NPM:-1}"

required_node_version="${AMM_REQUIRED_NODE_VERSION:-20.19.0}"

if ! command -v node >/dev/null 2>&1; then
  echo "AMM_web startup preflight failed: 'node' is not installed or not in PATH." >&2
  echo "Install Node.js >= ${required_node_version} for Reflex npm mode." >&2
  exit 78
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "AMM_web startup preflight failed: 'npm' is not installed or not in PATH." >&2
  echo "Install npm (usually provided with Node.js) and retry." >&2
  exit 78
fi

current_node_version="$(node -v | sed 's/^v//')"
lowest_version="$(printf '%s\n' "${required_node_version}" "${current_node_version}" | sort -V | head -n1)"
if [[ "${lowest_version}" != "${required_node_version}" ]]; then
  echo "AMM_web startup preflight failed: Node.js ${current_node_version} is too old." >&2
  echo "Required version is >= ${required_node_version}." >&2
  exit 78
fi

exec .venv/bin/reflex run \
  --env prod \
  --single-port \
  --frontend-port "${AMM_WEB_PORT:-3000}" \
  --backend-host "${AMM_WEB_HOST:-127.0.0.1}"
