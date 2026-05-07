"""WHERE-clause evaluator for the Mini Query Executor.

Evaluates a condition tree against a single row and returns True / False.

Condition format
────────────────
  Simple:    ("column", "op", value)      op ∈ {=, !=, <, >, <=, >=}
  IS NULL:   ("column", "IS", None)
  IS NOT:    ("column", "IS NOT", None)
  Logical:   ("AND", cond_left, cond_right)
             ("OR",  cond_left, cond_right)

Bug present (for students to find and fix):
  – E2  evaluate: ``=`` and ``!=`` do not guard against NULL.
        Python's ``None == None → True`` and ``None != 'x' → True``
        silently give wrong SQL semantics (SQL says any comparison with
        NULL yields NULL, which is falsy).  The ordering operators
        (``<``, ``>``, …) *do* guard against NULL because Python 3
        raises ``TypeError`` there — so the developer added a None
        check for those but forgot ``=`` / ``!=``.
"""
from __future__ import annotations

from typing import Any, Tuple, Union

from .table import Row

# A condition is either a simple 3-tuple or a logical 3-tuple.
Condition = Union[
    Tuple[str, str, Any],                # ("col", "op", value)
    Tuple[str, "Condition", "Condition"], # ("AND"/"OR", left, right)
]


class EvalError(Exception):
    """Raised when a condition cannot be evaluated."""


class Evaluator:
    """Stateless condition evaluator — call ``evaluate(row, condition)``."""

    def evaluate(self, row: Row, condition: Condition) -> bool:
        tag = condition[0]

        # ── logical connectives ───────────────────────────────────
        if tag == "AND":
            _, left, right = condition
            return self.evaluate(row, left) and self.evaluate(row, right)
        if tag == "OR":
            _, left, right = condition
            return self.evaluate(row, left) or self.evaluate(row, right)

        # ── simple comparison ─────────────────────────────────────
        column, op, value = condition
        row_val = row.get(column)

        # IS [NOT] NULL — always correct
        if op == "IS":
            return row_val is None
        if op == "IS NOT":
            return row_val is not None

        # Ordering operators: guard against None
        # (Python 3 raises TypeError on ``None < 5``)
        if op in ("<", ">", "<=", ">="):
            if row_val is None or value is None:
                return False
            if op == "<":
                return row_val < value
            if op == ">":
                return row_val > value
            if op == "<=":
                return row_val <= value
            return row_val >= value    # >=

        # BUG E2 ─────────────────────────────────────────────────
        # Python silently evaluates ``None == None → True`` and
        # ``None != 'active' → True``.  In SQL *any* comparison
        # involving NULL yields NULL (falsy).  The developer added
        # a None guard for ordering operators (which would crash)
        # but forgot = and != (which don't crash in Python).
        # ────────────────────────────────────────────────────────
        if op == "=":
            return row_val == value
        if op == "!=":
            return row_val != value

        raise EvalError(f"Unknown operator: {op!r}")
