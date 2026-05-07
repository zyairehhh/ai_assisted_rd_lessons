"""Recursive-descent parser for Mini SQL.

Converts a token list (from ``Lexer``) into an AST
(``SelectStatement | InsertStatement | …``).

Supported grammar
─────────────────
  SELECT cols FROM table [WHERE cond] [ORDER BY col [ASC|DESC]] [LIMIT n]
  INSERT INTO table (cols) VALUES (vals)
  UPDATE table SET col=val [, …] [WHERE cond]
  DELETE FROM table [WHERE cond]

  cond  ::= primary ( (AND|OR) primary )*
  primary ::= '(' cond ')' | comparison
  comparison ::= ident op literal | ident IS [NOT] NULL | ident LIKE literal

Bug present (for students to find and fix):
  – N1  _parse_primary_condition: parenthesised groups call _parse_comparison()
        instead of _parse_condition(), so nested parens and compound conditions
        inside parens fail.
"""
from __future__ import annotations

from typing import List, Optional

from .lexer import Token
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


class ParseError(Exception):
    """Raised when the token stream does not match the expected grammar."""


class Parser:
    """Recursive-descent parser.  Instantiate with a token list, then
    call ``parse()`` to obtain a single ``Statement``."""

    def __init__(self, tokens: List[Token]) -> None:
        self._tokens = tokens
        self._pos = 0

    # ── public ────────────────────────────────────────────────────

    def parse(self) -> Statement:
        kw = self._peek_keyword()
        if kw == "SELECT":
            return self._parse_select()
        if kw == "INSERT":
            return self._parse_insert()
        if kw == "UPDATE":
            return self._parse_update()
        if kw == "DELETE":
            return self._parse_delete()
        raise ParseError(f"Expected statement keyword, got {self._peek()!r}")

    # ── token helpers ─────────────────────────────────────────────

    def _peek(self) -> Token:
        if self._pos >= len(self._tokens):
            return Token("EOF", None)
        return self._tokens[self._pos]

    def _advance(self) -> Token:
        tok = self._peek()
        self._pos += 1
        return tok

    def _peek_keyword(self) -> Optional[str]:
        t = self._peek()
        return t.value if t.kind == "KEYWORD" else None

    def _peek_symbol(self) -> Optional[str]:
        t = self._peek()
        return t.value if t.kind == "SYMBOL" else None

    def _expect_keyword(self, value: str) -> Token:
        tok = self._advance()
        if tok.kind != "KEYWORD" or tok.value != value:
            raise ParseError(f"Expected keyword {value!r}, got {tok!r}")
        return tok

    def _expect_symbol(self, value: str) -> Token:
        tok = self._advance()
        if tok.kind != "SYMBOL" or tok.value != value:
            raise ParseError(f"Expected symbol {value!r}, got {tok!r}")
        return tok

    def _expect_identifier(self) -> Token:
        tok = self._advance()
        if tok.kind != "IDENTIFIER":
            raise ParseError(f"Expected identifier, got {tok!r}")
        return tok

    # ── SELECT ────────────────────────────────────────────────────

    def _parse_select(self) -> SelectStatement:
        self._expect_keyword("SELECT")
        columns = self._parse_column_list()
        self._expect_keyword("FROM")
        table = Identifier(self._expect_identifier().value)

        where = self._parse_optional_where()
        order_by = self._parse_optional_order_by()
        limit = self._parse_optional_limit()

        return SelectStatement(columns, table, where, order_by, limit)

    def _parse_column_list(self) -> list:
        if self._peek_symbol() == "*":
            self._advance()
            return [Star()]
        cols = [Identifier(self._expect_identifier().value)]
        while self._peek_symbol() == ",":
            self._advance()
            cols.append(Identifier(self._expect_identifier().value))
        return cols

    # ── INSERT ────────────────────────────────────────────────────

    def _parse_insert(self) -> InsertStatement:
        self._expect_keyword("INSERT")
        self._expect_keyword("INTO")
        table = Identifier(self._expect_identifier().value)

        self._expect_symbol("(")
        columns = [Identifier(self._expect_identifier().value)]
        while self._peek_symbol() == ",":
            self._advance()
            columns.append(Identifier(self._expect_identifier().value))
        self._expect_symbol(")")

        self._expect_keyword("VALUES")

        self._expect_symbol("(")
        values = [self._parse_literal()]
        while self._peek_symbol() == ",":
            self._advance()
            values.append(self._parse_literal())
        self._expect_symbol(")")

        return InsertStatement(table, columns, values)

    # ── UPDATE ────────────────────────────────────────────────────

    def _parse_update(self) -> UpdateStatement:
        self._expect_keyword("UPDATE")
        table = Identifier(self._expect_identifier().value)
        self._expect_keyword("SET")

        assignments = [self._parse_assignment()]
        while self._peek_symbol() == ",":
            self._advance()
            assignments.append(self._parse_assignment())

        where = self._parse_optional_where()
        return UpdateStatement(table, assignments, where)

    def _parse_assignment(self) -> Assignment:
        col = Identifier(self._expect_identifier().value)
        self._expect_symbol("=")
        val = self._parse_literal()
        return Assignment(col, val)

    # ── DELETE ────────────────────────────────────────────────────

    def _parse_delete(self) -> DeleteStatement:
        self._expect_keyword("DELETE")
        self._expect_keyword("FROM")
        table = Identifier(self._expect_identifier().value)
        where = self._parse_optional_where()
        return DeleteStatement(table, where)

    # ── WHERE / ORDER BY / LIMIT helpers ──────────────────────────

    def _parse_optional_where(self) -> Optional[Condition]:
        if self._peek_keyword() == "WHERE":
            self._advance()
            return self._parse_condition()
        return None

    def _parse_optional_order_by(self) -> Optional[OrderBy]:
        if self._peek_keyword() == "ORDER":
            self._advance()
            self._expect_keyword("BY")
            col = Identifier(self._expect_identifier().value)
            direction = "ASC"
            if self._peek_keyword() in ("ASC", "DESC"):
                direction = self._advance().value
            return OrderBy(col, direction)
        return None

    def _parse_optional_limit(self) -> Optional[int]:
        if self._peek_keyword() == "LIMIT":
            self._advance()
            tok = self._advance()
            if tok.kind != "INTEGER":
                raise ParseError(f"Expected integer after LIMIT, got {tok!r}")
            return tok.value
        return None

    # ── condition parsing ─────────────────────────────────────────

    def _parse_condition(self) -> Condition:
        left = self._parse_primary_condition()
        while self._peek_keyword() in ("AND", "OR"):
            op = self._advance().value
            right = self._parse_primary_condition()
            left = LogicalOp(op, left, right)
        return left

    def _parse_primary_condition(self) -> Condition:
        # Parenthesised group
        if self._peek_symbol() == "(":
            self._advance()
            # BUG N1: should be _parse_condition() to allow AND/OR and
            # nested parens inside the group, but calls _parse_comparison()
            # which only handles a single "ident op value" comparison.
            inner = self._parse_comparison()
            self._expect_symbol(")")
            return GroupedCondition(inner)
        return self._parse_comparison()

    def _parse_comparison(self) -> Condition:
        left_tok = self._expect_identifier()
        left = Identifier(left_tok.value)

        # IS [NOT] NULL
        if self._peek_keyword() == "IS":
            self._advance()
            negated = False
            if self._peek_keyword() == "NOT":
                self._advance()
                negated = True
            self._expect_keyword("NULL")
            return IsNull(left, negated)

        # LIKE
        if self._peek_keyword() == "LIKE":
            self._advance()
            right = self._parse_literal()
            return Comparison(left, "LIKE", right)

        # Comparison operators: =  !=  <  >  <=  >=
        op_tok = self._advance()
        if op_tok.kind != "SYMBOL" or op_tok.value not in (
            "=", "!=", "<", ">", "<=", ">=",
        ):
            raise ParseError(f"Expected comparison operator, got {op_tok!r}")
        right = self._parse_literal()
        return Comparison(left, op_tok.value, right)

    # ── literal parsing ───────────────────────────────────────────

    def _parse_literal(self) -> Literal:
        tok = self._advance()
        if tok.kind in ("INTEGER", "FLOAT", "STRING"):
            return Literal(tok.value)
        if tok.kind == "KEYWORD" and tok.value == "NULL":
            return Literal(None)
        raise ParseError(f"Expected literal value, got {tok!r}")
