#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────
# Mini SQL Parser — exercise validator
# ──────────────────────────────────────────────────────────────────
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PASS=0
FAIL=0

check() {
    local label="$1"; shift
    if "$@" > /dev/null 2>&1; then
        echo "  [OK]  $label"
        (( PASS++ ))
    else
        echo "  [FAIL] $label"
        (( FAIL++ ))
    fi
}

echo "=== L01 Mini SQL Parser validation ==="
echo ""

# 1. Unit tests (only minisql tests)
echo "── Unit tests ──"
PYTHONPATH="$ROOT_DIR/src" python3 -m unittest \
    tests.test_minisql_lexer tests.test_minisql_parser tests.test_minisql_formatter -v 2>&1 | tail -1
echo ""
if PYTHONPATH="$ROOT_DIR/src" python3 -m unittest \
    tests.test_minisql_lexer tests.test_minisql_parser tests.test_minisql_formatter 2>/dev/null; then
    echo "  [OK]  All unit tests pass"
    (( PASS++ ))
else
    echo "  [FAIL] Some unit tests still failing"
    (( FAIL++ ))
fi

# 2. Required artifacts
echo ""
echo "── Artifacts ──"
check "validation_report.md exists" test -f validation_report.md
check "context.md exists"           test -f context.md

# 3. validation_report.md structure (5 headings)
if [ -f validation_report.md ]; then
    HEADINGS=$(grep -cE '^#{1,3} ' validation_report.md || true)
    if [ "$HEADINGS" -ge 5 ]; then
        echo "  [OK]  validation_report.md has >= 5 section headings"
        (( PASS++ ))
    else
        echo "  [FAIL] validation_report.md has < 5 section headings (found $HEADINGS)"
        (( FAIL++ ))
    fi
fi

# 4. context.md not empty
if [ -f context.md ]; then
    LINES=$(wc -l < context.md | tr -d ' ')
    if [ "$LINES" -ge 5 ]; then
        echo "  [OK]  context.md has content (${LINES} lines)"
        (( PASS++ ))
    else
        echo "  [FAIL] context.md looks too short (${LINES} lines)"
        (( FAIL++ ))
    fi
fi

# Summary
echo ""
echo "── Summary ──"
echo "  PASS: $PASS   FAIL: $FAIL"
if [ "$FAIL" -eq 0 ]; then
    echo ""
    echo "  ✓ L01 Mini SQL Parser validation passed"
else
    echo ""
    echo "  ✗ $FAIL check(s) failed"
    exit 1
fi
