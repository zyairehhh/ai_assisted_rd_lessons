"""Tests for the Mini SQL formatter.

Baseline: ALL PASS — the formatter has no bugs.
These tests construct AST nodes directly, bypassing lexer and parser.
"""
import unittest

from minisql.formatter import Formatter
from minisql.ast_nodes import (
    Assignment,
    Comparison,
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
    UpdateStatement,
)


class FormatterTest(unittest.TestCase):

    def setUp(self):
        self.fmt = Formatter()

    # ── SELECT ────────────────────────────────────────────────────

    def test_select_star(self):
        stmt = SelectStatement([Star()], Identifier("users"))
        self.assertEqual(self.fmt.format(stmt), "SELECT * FROM users")

    def test_select_columns(self):
        stmt = SelectStatement(
            [Identifier("name"), Identifier("age")],
            Identifier("users"),
        )
        self.assertEqual(self.fmt.format(stmt), "SELECT name, age FROM users")

    def test_select_where(self):
        stmt = SelectStatement(
            [Star()],
            Identifier("t"),
            where=Comparison(Identifier("id"), "=", Literal(1)),
        )
        self.assertEqual(self.fmt.format(stmt), "SELECT * FROM t WHERE id = 1")

    def test_select_full(self):
        stmt = SelectStatement(
            [Identifier("name")],
            Identifier("t"),
            where=Comparison(Identifier("age"), ">", Literal(18)),
            order_by=OrderBy(Identifier("name"), "ASC"),
            limit=10,
        )
        self.assertEqual(
            self.fmt.format(stmt),
            "SELECT name FROM t WHERE age > 18 ORDER BY name ASC LIMIT 10",
        )

    # ── INSERT ────────────────────────────────────────────────────

    def test_insert(self):
        stmt = InsertStatement(
            Identifier("t"),
            [Identifier("a"), Identifier("b")],
            [Literal(1), Literal("hello")],
        )
        self.assertEqual(
            self.fmt.format(stmt),
            "INSERT INTO t (a, b) VALUES (1, 'hello')",
        )

    # ── UPDATE ────────────────────────────────────────────────────

    def test_update(self):
        stmt = UpdateStatement(
            Identifier("t"),
            [Assignment(Identifier("a"), Literal(42))],
            where=Comparison(Identifier("id"), "=", Literal(1)),
        )
        self.assertEqual(
            self.fmt.format(stmt),
            "UPDATE t SET a = 42 WHERE id = 1",
        )

    # ── DELETE ────────────────────────────────────────────────────

    def test_delete(self):
        stmt = DeleteStatement(
            Identifier("t"),
            where=Comparison(Identifier("id"), "=", Literal(1)),
        )
        self.assertEqual(
            self.fmt.format(stmt),
            "DELETE FROM t WHERE id = 1",
        )

    # ── conditions ────────────────────────────────────────────────

    def test_condition_and(self):
        cond = LogicalOp(
            "AND",
            Comparison(Identifier("a"), "=", Literal(1)),
            Comparison(Identifier("b"), "=", Literal(2)),
        )
        stmt = SelectStatement([Star()], Identifier("t"), where=cond)
        self.assertEqual(
            self.fmt.format(stmt),
            "SELECT * FROM t WHERE a = 1 AND b = 2",
        )

    def test_condition_is_null(self):
        stmt = SelectStatement(
            [Star()],
            Identifier("t"),
            where=IsNull(Identifier("email")),
        )
        self.assertEqual(
            self.fmt.format(stmt),
            "SELECT * FROM t WHERE email IS NULL",
        )

    def test_condition_grouped(self):
        cond = GroupedCondition(
            LogicalOp(
                "OR",
                Comparison(Identifier("a"), "=", Literal(1)),
                Comparison(Identifier("b"), "=", Literal(2)),
            )
        )
        stmt = SelectStatement([Star()], Identifier("t"), where=cond)
        self.assertEqual(
            self.fmt.format(stmt),
            "SELECT * FROM t WHERE (a = 1 OR b = 2)",
        )

    def test_null_literal(self):
        stmt = InsertStatement(
            Identifier("t"),
            [Identifier("a")],
            [Literal(None)],
        )
        self.assertEqual(
            self.fmt.format(stmt),
            "INSERT INTO t (a) VALUES (NULL)",
        )


if __name__ == "__main__":
    unittest.main()
