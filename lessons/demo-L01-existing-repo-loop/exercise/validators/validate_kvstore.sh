#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "[FAIL] $1" >&2
  exit 1
}

command -v python3 >/dev/null 2>&1 || fail "python3 is required"

PYTHONPATH="$ROOT_DIR/src" python3 -m unittest \
  tests.test_store tests.test_persistence tests.test_parser -v

[[ -s context.md ]] || fail "context.md is required and must be non-empty"
[[ -s validation_report.md ]] || fail "validation_report.md is required and must be non-empty"

for heading in \
  "## Initial Failure" \
  "## Root Cause" \
  "## Changes" \
  "## Validation" \
  "## Remaining Risks"; do
  grep -q "$heading" validation_report.md || fail "validation_report.md missing heading: $heading"
done

echo "[OK] L01 KVStore validation passed"
