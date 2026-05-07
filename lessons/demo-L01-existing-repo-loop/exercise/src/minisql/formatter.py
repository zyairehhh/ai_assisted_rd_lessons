"""SQL formatter — converts an AST back to a canonical SQL string.

DO NOT MODIFY — this module has no bugs and is not in scope.
"""
from __future__ import annotations

from .ast_nodes import (
    Assignment,
    Comparison,
    Condition,
    DeleteStatement,
    GroupedCondition,
    Identifier,
    InsertStatement,
    IsNull,
    Literal,
    LogicalOp,
    OrderBy,
    SelectStatement,
    Star,
    Statement,
    UpdateStatement,
)


class Formatter:
    """Formats a ``Statement`` AST back into a SQL string."""

    def format(self, stmt: Statement) -> str:
        if isinstance(stmt, SelectStatement):
            return self._fmt_select(stmt)
        if isinstance(stmt, InsertStatement):
            return self._fmt_insert(stmt)
        if isinstance(stmt, UpdateStatement):
            return self._fmt_update(stmt)
        if isinstance(stmt, DeleteStatement):
            return self._fmt_delete(stmt)
        raise TypeError(f"Unknown statement type: {type(stmt).__name__}")

    # ── statements ────────────────────────────────────────────────

    def _fmt_select(self, s: SelectStatement) -> str:
        cols = ", ".join(self._fmt_column(c) for c in s.columns)
        parts = [f"SELECT {cols} FROM {s.table.name}"]
        if s.where is not None:
            parts.append(f"WHERE {self._fmt_cond(s.where)}")
        if s.order_by is not None:
            parts.append(
                f"ORDER BY {s.order_by.column.name} {s.order_by.direction}"
            )
        if s.limit is not None:
            parts.append(f"LIMIT {s.limit}")
        return " ".join(parts)

    def _fmt_insert(self, s: InsertStatement) -> str:
        cols = ", ".join(c.name for c in s.columns)
        vals = ", ".join(self._fmt_value(v) for v in s.values)
        return f"INSERT INTO {s.table.name} ({cols}) VALUES ({vals})"

    def _fmt_update(self, s: UpdateStatement) -> str:
        sets = ", ".join(
            f"{a.column.name} = {self._fmt_value(a.value)}"
            for a in s.assignments
        )
        sql = f"UPDATE {s.table.name} SET {sets}"
        if s.where is not None:
            sql += f" WHERE {self._fmt_cond(s.where)}"
        return sql

    def _fmt_delete(self, s: DeleteStatement) -> str:
        sql = f"DELETE FROM {s.table.name}"
        if s.where is not None:
            sql += f" WHERE {self._fmt_cond(s.where)}"
        return sql

    # ── helpers ───────────────────────────────────────────────────

    @staticmethod
    def _fmt_column(c) -> str:
        if isinstance(c, Star):
            return "*"
        return c.name

    def _fmt_cond(self, c: Condition) -> str:
        if isinstance(c, Comparison):
            return f"{c.left.name} {c.op} {self._fmt_value(c.right)}"
        if isinstance(c, IsNull):
            neg = " NOT" if c.negated else ""
            return f"{c.column.name} IS{neg} NULL"
        if isinstance(c, LogicalOp):
            return f"{self._fmt_cond(c.left)} {c.op} {self._fmt_cond(c.right)}"
        if isinstance(c, GroupedCondition):
            return f"({self._fmt_cond(c.inner)})"
        raise TypeError(f"Unknown condition type: {type(c).__name__}")

    @staticmethod
    def _fmt_value(v) -> str:
        if isinstance(v, Literal):
            if v.value is None:
                return "NULL"
            if isinstance(v.value, str):
                return f"'{v.value}'"
            return str(v.value)
        if isinstance(v, Identifier):
            return v.name
        return str(v)
