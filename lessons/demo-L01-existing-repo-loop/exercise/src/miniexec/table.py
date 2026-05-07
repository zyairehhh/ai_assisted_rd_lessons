"""In-memory table representation.

DO NOT MODIFY — this is the shared data model used by evaluator and executor.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


Row = dict[str, Any]
"""A single row: column name → value.  ``None`` represents SQL NULL."""


@dataclass
class Table:
    """A named, column-typed, in-memory table.

    Rows are plain dicts.  The executor trusts that callers only insert
    rows whose keys are a subset of ``columns``.
    """
    name: str
    columns: list[str]
    rows: list[Row] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Defensive copy so the caller's list is not aliased.
        self.columns = list(self.columns)
        self.rows = [dict(r) for r in self.rows]

    def copy(self) -> "Table":
        """Return a deep-enough copy (rows are shallow-copied)."""
        return Table(self.name, list(self.columns), [dict(r) for r in self.rows])

    def __len__(self) -> int:
        return len(self.rows)

    def __repr__(self) -> str:
        return f"Table({self.name!r}, cols={self.columns}, {len(self.rows)} rows)"
