"""AST node definitions for Mini SQL parser.

DO NOT MODIFY — these are the shared data structures used by lexer,
parser, and formatter.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union


# ── Atoms ─────────────────────────────────────────────────────────

@dataclass
class Literal:
    """A literal value: integer, float, string, or NULL."""
    value: Union[int, float, str, None]

    def __repr__(self) -> str:
        if self.value is None:
            return "Literal(NULL)"
        return f"Literal({self.value!r})"


@dataclass
class Identifier:
    """A column or table name."""
    name: str


@dataclass
class Star:
    """Represents ``SELECT *``."""
    pass


# ── Conditions ────────────────────────────────────────────────────

@dataclass
class Comparison:
    left: Identifier
    op: str                          # =, !=, <, >, <=, >=, LIKE
    right: Union[Literal, Identifier]


@dataclass
class IsNull:
    column: Identifier
    negated: bool = False            # True → IS NOT NULL


@dataclass
class LogicalOp:
    op: str                          # AND | OR
    left: "Condition"
    right: "Condition"


@dataclass
class GroupedCondition:
    """A parenthesised condition group: ``(cond)``."""
    inner: "Condition"


Condition = Union[Comparison, IsNull, LogicalOp, GroupedCondition]


# ── Clauses ───────────────────────────────────────────────────────

@dataclass
class OrderBy:
    column: Identifier
    direction: str = "ASC"           # ASC | DESC


@dataclass
class Assignment:
    """``SET col = val``."""
    column: Identifier
    value: Union[Literal, Identifier]


# ── Statements ────────────────────────────────────────────────────

@dataclass
class SelectStatement:
    columns: list                    # list[Identifier | Star]
    table: Identifier
    where: Union[Condition, None] = None
    order_by: Union[OrderBy, None] = None
    limit: Union[int, None] = None


@dataclass
class InsertStatement:
    table: Identifier
    columns: list                    # list[Identifier]
    values: list                     # list[Literal]


@dataclass
class UpdateStatement:
    table: Identifier
    assignments: list                # list[Assignment]
    where: Union[Condition, None] = None


@dataclass
class DeleteStatement:
    table: Identifier
    where: Union[Condition, None] = None


Statement = Union[SelectStatement, InsertStatement, UpdateStatement, DeleteStatement]
