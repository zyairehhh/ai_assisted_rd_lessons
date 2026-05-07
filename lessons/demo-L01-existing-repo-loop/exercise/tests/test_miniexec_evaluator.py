"""Tests for the Mini Query Executor — evaluator module.

Baseline: 2 FAIL  (EvaluatorNullTest)  /  rest PASS
"""
import unittest

from miniexec.evaluator import Evaluator


class EvaluatorBasicTest(unittest.TestCase):
    """Basic condition evaluation — all pass."""

    def setUp(self):
        self.ev = Evaluator()
        self.row = {"id": 1, "name": "alice", "age": 25, "email": None}

    def test_equal_match(self):
        self.assertTrue(self.ev.evaluate(self.row, ("age", "=", 25)))

    def test_equal_no_match(self):
        self.assertFalse(self.ev.evaluate(self.row, ("age", "=", 30)))

    def test_not_equal(self):
        self.assertTrue(self.ev.evaluate(self.row, ("age", "!=", 30)))

    def test_less_than(self):
        self.assertTrue(self.ev.evaluate(self.row, ("age", "<", 30)))

    def test_greater_than(self):
        self.assertTrue(self.ev.evaluate(self.row, ("age", ">", 20)))

    def test_less_equal(self):
        self.assertTrue(self.ev.evaluate(self.row, ("age", "<=", 25)))

    def test_greater_equal(self):
        self.assertTrue(self.ev.evaluate(self.row, ("age", ">=", 25)))

    def test_is_null_true(self):
        self.assertTrue(self.ev.evaluate(self.row, ("email", "IS", None)))

    def test_is_null_false(self):
        self.assertFalse(self.ev.evaluate(self.row, ("name", "IS", None)))

    def test_is_not_null(self):
        self.assertTrue(self.ev.evaluate(self.row, ("name", "IS NOT", None)))

    def test_and_both_true(self):
        cond = ("AND", ("age", ">", 20), ("name", "=", "alice"))
        self.assertTrue(self.ev.evaluate(self.row, cond))

    def test_and_one_false(self):
        cond = ("AND", ("age", ">", 20), ("name", "=", "bob"))
        self.assertFalse(self.ev.evaluate(self.row, cond))

    def test_or_one_true(self):
        cond = ("OR", ("age", ">", 100), ("name", "=", "alice"))
        self.assertTrue(self.ev.evaluate(self.row, cond))

    def test_or_both_false(self):
        cond = ("OR", ("age", ">", 100), ("name", "=", "bob"))
        self.assertFalse(self.ev.evaluate(self.row, cond))


class EvaluatorNullTest(unittest.TestCase):
    """NULL semantics — 2 tests FAIL due to Bug E2."""

    def setUp(self):
        self.ev = Evaluator()
        self.null_row = {"id": 1, "status": None, "age": None}
        self.normal_row = {"id": 2, "status": "active", "age": 30}

    # ── FAILING: Bug E2 ──────────────────────────────────────────

    def test_equal_null_not_matched(self):
        """In SQL, ``col = NULL`` never matches — NULL = NULL is NULL (falsy).

        BUG E2: Python's ``None == None`` returns True, so the
        evaluator incorrectly says this row matches.
        """
        result = self.ev.evaluate(self.null_row, ("status", "=", None))
        self.assertFalse(result)

    def test_not_equal_skips_null_rows(self):
        """In SQL, ``col != 'active'`` skips rows where col is NULL.

        NULL != 'active' is NULL (falsy) in SQL, not True.

        BUG E2: Python's ``None != 'active'`` returns True, so the
        evaluator incorrectly includes NULL rows.
        """
        result = self.ev.evaluate(self.null_row, ("status", "!=", "active"))
        self.assertFalse(result)

    # ── PASSING ───────────────────────────────────────────────────

    def test_is_null_still_works(self):
        """IS NULL is the correct way to test for NULL — works fine."""
        self.assertTrue(self.ev.evaluate(self.null_row, ("status", "IS", None)))

    def test_is_not_null_on_null_row(self):
        self.assertFalse(self.ev.evaluate(self.null_row, ("status", "IS NOT", None)))

    def test_less_than_with_null_returns_false(self):
        """Ordering operators already handle NULL correctly."""
        self.assertFalse(self.ev.evaluate(self.null_row, ("age", "<", 10)))

    def test_greater_than_with_null_returns_false(self):
        self.assertFalse(self.ev.evaluate(self.null_row, ("age", ">", 10)))

    def test_equal_normal_row_still_works(self):
        """Non-NULL = should still work."""
        self.assertTrue(self.ev.evaluate(self.normal_row, ("status", "=", "active")))

    def test_not_equal_normal_row_still_works(self):
        self.assertTrue(self.ev.evaluate(self.normal_row, ("status", "!=", "pending")))


if __name__ == "__main__":
    unittest.main()
