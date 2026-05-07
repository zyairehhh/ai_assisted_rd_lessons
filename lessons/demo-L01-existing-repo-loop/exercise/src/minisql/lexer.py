"""Tokeniser for Mini SQL.

Converts a raw SQL string into a list of ``Token`` objects.

Bugs present (for students to find and fix):
  – T1  _split:    does not track quote state → spaces inside strings split the token
  – T3  _classify: digit-only string content misclassified as INTEGER
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

KEYWORDS = frozenset({
    "SELECT", "FROM", "WHERE", "AND", "OR", "NOT",
    "INSERT", "INTO", "VALUES",
    "UPDATE", "SET",
    "DELETE",
    "ORDER", "BY", "ASC", "DESC",
    "LIMIT",
    "IS", "NULL", "LIKE",
})

SYMBOLS = {"(", ")", ",", "=", "!=", "<", ">", "<=", ">=", "*"}


@dataclass
class Token:
    kind: str          # KEYWORD | IDENTIFIER | INTEGER | FLOAT | STRING | SYMBOL
    value: object

    def __repr__(self) -> str:
        return f"Token({self.kind}, {self.value!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return NotImplemented
        return self.kind == other.kind and self.value == other.value


class LexError(Exception):
    """Raised when an unrecognisable token is encountered."""


class Lexer:
    """Stateless tokeniser — call ``tokenize(sql)`` for each statement."""

    def tokenize(self, sql: str) -> List[Token]:
        raw_parts = self._split(sql)
        return [self._classify(part) for part in raw_parts]

    # ── splitting ─────────────────────────────────────────────────

    def _split(self, sql: str) -> List[str]:
        """Split *sql* into raw token strings.

        BUG T1: this method does **not** track whether the current
        position is inside a quoted string, so a space inside
        ``'John Doe'`` produces two fragments ``"'John"`` and ``"Doe'"``.
        """
        tokens: List[str] = []
        current = ""
        i = 0
        while i < len(sql):
            ch = sql[i]

            # Two-character operators: !=  <=  >=
            if ch in "!<>" and i + 1 < len(sql) and sql[i + 1] == "=":
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append(ch + "=")
                i += 2
                continue

            # Single-character symbols
            if ch in "(),=<>*":
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append(ch)
                i += 1
                continue

            # Whitespace — splits even when inside quotes (BUG T1)
            if ch in " \t\n\r":
                if current:
                    tokens.append(current)
                    current = ""
                i += 1
                continue

            current += ch
            i += 1

        if current:
            tokens.append(current)
        return tokens

    # ── classification ────────────────────────────────────────────

    def _classify(self, raw: str) -> Token:
        """Turn a raw string fragment into a typed ``Token``.

        BUG T3: a single-quoted token whose content is purely digits
        (e.g. ``'123'``) is returned as ``Token('INTEGER', 123)``
        instead of ``Token('STRING', '123')``.
        """
        upper = raw.upper()

        # Symbols
        if raw in SYMBOLS:
            return Token("SYMBOL", raw)

        # String literals — single-quoted
        if raw.startswith("'") and raw.endswith("'") and len(raw) >= 2:
            content = raw[1:-1]
            # BUG T3: digit-only string content → INTEGER
            if content.isdigit():
                return Token("INTEGER", int(content))
            return Token("STRING", content)

        # Keywords
        if upper in KEYWORDS:
            return Token("KEYWORD", upper)

        # Numeric literals
        if self._is_integer(raw):
            return Token("INTEGER", int(raw))
        if self._is_float(raw):
            return Token("FLOAT", float(raw))

        # Identifiers (plain or double-quoted)
        if self._is_identifier(raw):
            return Token("IDENTIFIER", raw)

        raise LexError(f"Unexpected token: {raw!r}")

    # ── helpers ───────────────────────────────────────────────────

    @staticmethod
    def _is_integer(s: str) -> bool:
        if s.startswith("-"):
            return len(s) > 1 and s[1:].isdigit()
        return s.isdigit()

    @staticmethod
    def _is_float(s: str) -> bool:
        if "." not in s:
            return False
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_identifier(s: str) -> bool:
        if s.isidentifier():
            return True
        # Double-quoted identifiers: "my column"
        return len(s) >= 2 and s.startswith('"') and s.endswith('"')
