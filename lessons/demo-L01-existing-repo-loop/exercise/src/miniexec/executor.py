"""Mini Query Executor — executes queries on in-memory tables.

Supported operations
────────────────────
  select   — projection, filtering, sorting, limit/offset
  insert   — append a row
  update   — modify matching rows
  delete   — remove matching rows
  aggregate — COUNT / SUM / AVG / MIN / MAX

Bugs present (for students to find and fix):
  – E1  _apply_limit:  ``rows[start:limit]`` instead of
        ``rows[start:start + limit]`` — OFFSET+LIMIT returns too few rows.
  – E3  aggregate:  ``COUNT(column)`` counts all rows instead of
        skipping NULLs; behaves identically to ``COUNT(*)``.
"""
from __future__ import annotations

from typing import Any, Optional

from .evaluator import Condition, Evaluator
from .table import Row, Table


class Executor:
    """Stateful only in that it holds an ``Evaluator``; each method
    operates directly on the ``Table`` passed to it."""

    def __init__(self) -> None:
        self._evaluator = Evaluator()

    # ── SELECT ────────────────────────────────────────────────────

    def select(
        self,
        table: Table,
        columns: Optional[list[str]] = None,
        where: Optional[Condition] = None,
        order_by: Optional[tuple[str, str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[Row]:
        """Return rows matching *where*, projected to *columns*."""
        rows = list(table.rows)

        if where is not None:
            rows = [r for r in rows if self._evaluator.evaluate(r, where)]

        if order_by is not None:
            col, direction = order_by
            rows = self._sort_rows(rows, col, direction)

        if limit is not None or offset is not None:
            rows = self._apply_limit(rows, limit, offset)

        return self._project(rows, columns)

    # ── INSERT ────────────────────────────────────────────────────

    def insert(self, table: Table, row: Row) -> int:
        """Append *row* to *table*.  Returns 1."""
        table.rows.append(dict(row))
        return 1

    # ── UPDATE ────────────────────────────────────────────────────

    def update(
        self,
        table: Table,
        assignments: dict[str, Any],
        where: Optional[Condition] = None,
    ) -> int:
        """Update matching rows.  Returns number of rows modified."""
        count = 0
        for row in table.rows:
            if where is None or self._evaluator.evaluate(row, where):
                row.update(assignments)
                count += 1
        return count

    # ── DELETE ────────────────────────────────────────────────────

    def delete(
        self,
        table: Table,
        where: Optional[Condition] = None,
    ) -> int:
        """Remove matching rows.  Returns number of rows removed."""
        if where is None:
            count = len(table.rows)
            table.rows.clear()
            return count
        before = len(table.rows)
        table.rows[:] = [
            r for r in table.rows
            if not self._evaluator.evaluate(r, where)
        ]
        return before - len(table.rows)

    # ── AGGREGATE ─────────────────────────────────────────────────

    def aggregate(
        self,
        table: Table,
        func: str,
        column: Optional[str] = None,
        where: Optional[Condition] = None,
    ) -> Any:
        """Compute an aggregate function over *column*.

        *func* is one of COUNT, SUM, AVG, MIN, MAX.
        ``column=None`` or ``column="*"`` means "all rows" (only valid
        for COUNT).
        """
        rows = list(table.rows)
        if where is not None:
            rows = [r for r in rows if self._evaluator.evaluate(r, where)]

        if func == "COUNT":
            if column is None or column == "*":
                return len(rows)
            # BUG E3: counts all rows, should skip rows where
            # column is NULL.  ``COUNT(col)`` ≠ ``COUNT(*)``.
            return len(rows)

        # Other aggregates: extract non-NULL values from the column
        values = [r[column] for r in rows if r.get(column) is not None]

        if func == "SUM":
            return sum(values) if values else None
        if func == "AVG":
            return sum(values) / len(values) if values else None
        if func == "MIN":
            return min(values) if values else None
        if func == "MAX":
            return max(values) if values else None

        raise ValueError(f"Unknown aggregate function: {func!r}")

    # ── internal helpers ──────────────────────────────────────────

    @staticmethod
    def _sort_rows(rows: list[Row], column: str, direction: str) -> list[Row]:
        """Sort rows by *column*.  NULLs sort last for ASC, first for DESC."""
        def sort_key(row: Row):
            val = row.get(column)
            if val is None:
                return (1, "")   # NULLs last
            return (0, val)
        return sorted(rows, key=sort_key, reverse=(direction == "DESC"))

    @staticmethod
    def _apply_limit(
        rows: list[Row],
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[Row]:
        """Apply OFFSET and LIMIT to *rows*.

        BUG E1: uses ``rows[start:limit]`` instead of
        ``rows[start:start + limit]``.  When offset > 0 and limit is
        given, the slice end is wrong — returning fewer rows than
        requested (or an empty list when offset ≥ limit).
        """
        start = offset or 0
        if limit is not None:
            return rows[start:limit]     # BUG: should be rows[start:start + limit]
        return rows[start:]

    @staticmethod
    def _project(rows: list[Row], columns: Optional[list[str]]) -> list[Row]:
        """Project rows to a subset of columns.  ``None`` → all columns."""
        if columns is None:
            return [dict(r) for r in rows]
        return [{c: r.get(c) for c in columns} for r in rows]
