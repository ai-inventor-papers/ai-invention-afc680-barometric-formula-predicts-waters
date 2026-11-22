#!/usr/bin/env bash
# Recreates the deleted Python environment (.venv/) with the exact pinned versions in requirements.txt.
set -euo pipefail
cd "$(dirname "$0")"
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r requirements.txt
