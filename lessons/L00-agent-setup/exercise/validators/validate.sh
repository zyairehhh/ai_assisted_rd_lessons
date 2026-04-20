#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "[FAIL] $1" >&2
  exit 1
}

warn() {
  echo "[WARN] $1" >&2
}

command -v python3 >/dev/null 2>&1 || fail "python3 is required"
command -v git >/dev/null 2>&1 || fail "git is required"

if command -v opencode >/dev/null 2>&1; then
  echo "[OK] opencode found"
else
  warn "opencode not found"
fi

if command -v codex >/dev/null 2>&1; then
  echo "[OK] codex found"
else
  warn "codex not found"
fi

if command -v cursor >/dev/null 2>&1; then
  echo "[OK] cursor found"
else
  warn "cursor not found"
fi

[[ -s context.md ]] || fail "context.md is required and must be non-empty"
[[ -s agent_setup_report.md ]] || fail "agent_setup_report.md is required and must be non-empty"

for heading in \
  "## Tool" \
  "## Model Configuration" \
  "## Basic Prompt Trial" \
  "## Skill Installation" \
  "## Problems" \
  "## Next Actions"; do
  grep -q "$heading" agent_setup_report.md || fail "agent_setup_report.md missing heading: $heading"
done

if grep -Eqi "(api[_ -]?key|token|password|secret)[[:space:]]*[:=][[:space:]]*[^[:space:]]+" agent_setup_report.md context.md; then
  fail "possible secret found in report or context"
fi

echo "[OK] L00 environment report validation passed"
