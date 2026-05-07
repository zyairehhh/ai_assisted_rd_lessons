"""Tests for the Mini SQL parser.

Baseline: 3 FAIL  (ParserConditionGroupTest × 2 + ParserInsertTest × 1)
          all others PASS
"""
import unittest

from minisql import parse
from minisql.ast_nodes import (
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


# ═══════════════════════════════════════════════════════════════════
# SELECT
# ═══════════════════════════════════════════════════════════════════

class ParserSelectTest(unittest.TestCase):
    """All of these tests pass."""

    def test_select_star(self):
        stmt = parse("SELECT * FROM users")
        self.assertIsInstance(stmt, SelectStatement)
        self.assertEqual(len(stmt.columns), 1)
        self.assertIsInstance(stmt.columns[0], Star)
        self.assertEqual(stmt.table.name, "users")

    def test_select_columns(self):
        stmt = parse("SELECT name, age FROM users")
        self.assertEqual([c.name for c in stmt.columns], ["name", "age"])

    def test_select_where_eq(self):
        stmt = parse("SELECT * FROM users WHERE id = 1")
        self.assertIsInstance(stmt.where, Comparison)
        self.assertEqual(stmt.where.left.name, "id")
        self.assertEqual(stmt.where.op, "=")
        self.assertEqual(stmt.where.right.value, 1)

    def test_select_where_and(self):
        stmt = parse("SELECT * FROM t WHERE a = 1 AND b = 2")
        self.assertIsInstance(stmt.where, LogicalOp)
        self.assertEqual(stmt.where.op, "AND")

    def test_select_where_string(self):
        stmt = parse("SELECT * FROM t WHERE name = 'alice'")
        self.assertEqual(stmt.where.right.value, "alice")

    def test_select_order_by_asc(self):
        stmt = parse("SELECT * FROM t ORDER BY name ASC")
        self.assertIsNotNone(stmt.order_by)
        self.assertEqual(stmt.order_by.column.name, "name")
        self.assertEqual(stmt.order_by.direction, "ASC")

    def test_select_order_by_desc(self):
        stmt = parse("SELECT * FROM t ORDER BY id DESC")
        self.assertEqual(stmt.order_by.direction, "DESC")

    def test_select_limit(self):
        stmt = parse("SELECT * FROM t LIMIT 10")
        self.assertEqual(stmt.limit, 10)

    def test_select_full(self):
        stmt = parse(
            "SELECT name, age FROM users WHERE age > 18 ORDER BY name ASC LIMIT 5"
        )
        self.assertIsInstance(stmt, SelectStatement)
        self.assertEqual(len(stmt.columns), 2)
        self.assertIsInstance(stmt.where, Comparison)
        self.assertIsNotNone(stmt.order_by)
        self.assertEqual(stmt.limit, 5)

    def test_select_is_null(self):
        stmt = parse("SELECT * FROM t WHERE email IS NULL")
        self.assertIsInstance(stmt.where, IsNull)
        self.assertFalse(stmt.where.negated)

    def test_select_is_not_null(self):
        stmt = parse("SELECT * FROM t WHERE email IS NOT NULL")
        self.assertIsInstance(stmt.where, IsNull)
        self.assertTrue(stmt.where.negated)

    def test_select_like(self):
        stmt = parse("SELECT * FROM t WHERE name LIKE 'A%'")
        self.assertIsInstance(stmt.where, Comparison)
        self.assertEqual(stmt.where.op, "LIKE")


# ═══════════════════════════════════════════════════════════════════
# Condition grouping  (parenthesised WHERE)
# ═══════════════════════════════════════════════════════════════════

class ParserConditionGroupTest(unittest.TestCase):
    """Parenthesised conditions — 2 tests FAIL due to Bug N1."""

    def test_simple_parens(self):
        """Single comparison inside parens — works even with the bug."""
        stmt = parse("SELECT * FROM t WHERE (a = 1)")
        self.assertIsInstance(stmt.where, GroupedCondition)
        self.assertIsInstance(stmt.where.inner, Comparison)

    # ── FAILING: Bug N1 ──────────────────────────────────────────

    def test_nested_parens(self):
        """Double-nested parens: ((a = 1)).

        BUG N1: the outer '(' dispatches to _parse_comparison() which
        expects an identifier but hits the inner '(' → ParseError.
        """
        stmt = parse("SELECT * FROM t WHERE ((a = 1))")
        self.assertIsInstance(stmt.where, GroupedCondition)
        inner = stmt.where.inner
        self.assertIsInstance(inner, GroupedCondition)
        self.assertIsInstance(inner.inner, Comparison)

    def test_compound_in_parens(self):
        """Compound condition inside parens: (a = 1 AND b = 2).

        BUG N1: _parse_comparison() parses 'a = 1' then expects ')'
        but finds AND → ParseError.
        """
        stmt = parse("SELECT * FROM t WHERE (a = 1 AND b = 2)")
        self.assertIsInstance(stmt.where, GroupedCondition)
        self.assertIsInstance(stmt.where.inner, LogicalOp)
        self.assertEqual(stmt.where.inner.op, "AND")

    # ── PASSING ───────────────────────────────────────────────────

    def test_parens_with_or(self):
        """Top-level OR with a simple paren group — passes."""
        stmt = parse("SELECT * FROM t WHERE a = 1 OR (b = 2)")
        self.assertIsInstance(stmt.where, LogicalOp)
        self.assertEqual(stmt.where.op, "OR")
        self.assertIsInstance(stmt.where.right, GroupedCondition)


# ═══════════════════════════════════════════════════════════════════
# INSERT
# ═══════════════════════════════════════════════════════════════════

class ParserInsertTest(unittest.TestCase):
    """INSERT parsing — 1 test FAILS (T1 propagated from lexer)."""

    def test_insert_integers(self):
        stmt = parse("INSERT INTO t (a, b) VALUES (1, 2)")
        self.assertIsInstance(stmt, InsertStatement)
        self.assertEqual(stmt.table.name, "t")
        self.assertEqual(len(stmt.columns), 2)
        self.assertEqual(len(stmt.values), 2)
        self.assertEqual(stmt.values[0].value, 1)

    def test_insert_null(self):
        stmt = parse("INSERT INTO t (a) VALUES (NULL)")
        self.assertIsNone(stmt.values[0].value)

    # ── FAILING: Bug T1 propagated ────────────────────────────────

    def test_insert_string_with_space(self):
        """INSERT with a string value that contains a space.

        BUG T1 (lexer): the space inside 'John Doe' splits the token,
        causing a LexError before the parser even runs.
        """
        stmt = parse("INSERT INTO users (name) VALUES ('John Doe')")
        self.assertIsInstance(stmt, InsertStatement)
        self.assertEqual(len(stmt.values), 1)
        self.assertEqual(stmt.values[0].value, "John Doe")


# ═══════════════════════════════════════════════════════════════════
# UPDATE
# ═══════════════════════════════════════════════════════════════════

class ParserUpdateTest(unittest.TestCase):

    def test_update_basic(self):
        stmt = parse("UPDATE t SET a = 1")
        self.assertIsInstance(stmt, UpdateStatement)
        self.assertEqual(stmt.table.name, "t")
        self.assertEqual(len(stmt.assignments), 1)
        self.assertEqual(stmt.assignments[0].column.name, "a")

    def test_update_multiple_set(self):
        stmt = parse("UPDATE t SET a = 1, b = 2")
        self.assertEqual(len(stmt.assignments), 2)

    def test_update_where(self):
        stmt = parse("UPDATE t SET name = 'bob' WHERE id = 1")
        self.assertIsNotNone(stmt.where)
        self.assertIsInstance(stmt.where, Comparison)


# ═══════════════════════════════════════════════════════════════════
# DELETE
# ═══════════════════════════════════════════════════════════════════

class ParserDeleteTest(unittest.TestCase):

    def test_delete_all(self):
        stmt = parse("DELETE FROM t")
        self.assertIsInstance(stmt, DeleteStatement)
        self.assertEqual(stmt.table.name, "t")
        self.assertIsNone(stmt.where)

    def test_delete_where(self):
        stmt = parse("DELETE FROM t WHERE id = 1")
        self.assertIsNotNone(stmt.where)
        self.assertIsInstance(stmt.where, Comparison)


if __name__ == "__main__":
    unittest.main()
