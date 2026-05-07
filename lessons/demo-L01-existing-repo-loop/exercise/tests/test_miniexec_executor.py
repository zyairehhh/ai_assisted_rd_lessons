"""Tests for the Mini Query Executor — executor module.

Baseline: 3 FAIL  (LimitOffset × 2 + Aggregate × 1)  /  rest PASS
"""
import unittest

from miniexec.executor import Executor
from miniexec.table import Table


def _id_table(n: int = 5) -> Table:
    """Helper: table with rows id=1..n."""
    return Table("t", ["id"], [{"id": i} for i in range(1, n + 1)])


def _people_table() -> Table:
    return Table("people", ["id", "name", "age", "status"], [
        {"id": 1, "name": "alice", "age": 30, "status": "active"},
        {"id": 2, "name": "bob",   "age": 25, "status": "active"},
        {"id": 3, "name": "carol", "age": 35, "status": "inactive"},
        {"id": 4, "name": "dave",  "age": 28, "status": None},
        {"id": 5, "name": "eve",   "age": None, "status": None},
    ])


# ═══════════════════════════════════════════════════════════════════
# SELECT basics
# ═══════════════════════════════════════════════════════════════════

class ExecutorSelectTest(unittest.TestCase):
    """Basic SELECT — all pass."""

    def setUp(self):
        self.ex = Executor()
        self.t = _people_table()

    def test_select_all(self):
        rows = self.ex.select(self.t)
        self.assertEqual(len(rows), 5)

    def test_select_columns(self):
        rows = self.ex.select(self.t, columns=["name", "age"])
        self.assertEqual(set(rows[0].keys()), {"name", "age"})

    def test_select_where(self):
        rows = self.ex.select(self.t, where=("age", ">", 28))
        names = [r["name"] for r in rows]
        self.assertEqual(sorted(names), ["alice", "carol"])

    def test_select_where_and(self):
        cond = ("AND", ("age", ">", 25), ("status", "=", "active"))
        rows = self.ex.select(self.t, where=cond)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], "alice")

    def test_select_order_by_asc(self):
        rows = self.ex.select(self.t, columns=["name"], order_by=("name", "ASC"))
        names = [r["name"] for r in rows]
        self.assertEqual(names[:3], ["alice", "bob", "carol"])

    def test_select_order_by_desc(self):
        rows = self.ex.select(self.t, columns=["name"], order_by=("name", "DESC"))
        # NULLs sort first for DESC (reversed from last)
        self.assertEqual(rows[-1]["name"], "alice")

    def test_select_order_by_nulls_last_asc(self):
        """NULLs in sorted column go to the end for ASC."""
        rows = self.ex.select(self.t, columns=["name", "age"], order_by=("age", "ASC"))
        # Last row should be the NULL-age row (eve)
        self.assertIsNone(rows[-1]["age"])


# ═══════════════════════════════════════════════════════════════════
# LIMIT / OFFSET
# ═══════════════════════════════════════════════════════════════════

class ExecutorLimitOffsetTest(unittest.TestCase):
    """LIMIT and OFFSET — 2 tests FAIL due to Bug E1."""

    def setUp(self):
        self.ex = Executor()
        self.t = _id_table(5)   # rows: id=1,2,3,4,5

    def test_limit_only(self):
        """LIMIT without OFFSET works (offset defaults to 0)."""
        rows = self.ex.select(self.t, limit=2)
        self.assertEqual([r["id"] for r in rows], [1, 2])

    def test_offset_only(self):
        """OFFSET without LIMIT returns the rest."""
        rows = self.ex.select(self.t, offset=3)
        self.assertEqual([r["id"] for r in rows], [4, 5])

    # ── FAILING: Bug E1 ──────────────────────────────────────────

    def test_limit_with_offset(self):
        """LIMIT 2 OFFSET 1 should return 2 rows starting at row index 1.

        Expected: [2, 3]  (rows[1:3])
        BUG E1:  rows[1:2] → [2] (only 1 row) because the code
        uses ``rows[start:limit]`` instead of ``rows[start:start+limit]``.
        """
        rows = self.ex.select(self.t, limit=2, offset=1)
        ids = [r["id"] for r in rows]
        self.assertEqual(ids, [2, 3])

    def test_offset_past_limit_value(self):
        """LIMIT 2 OFFSET 3 should return [4, 5].

        BUG E1: ``rows[3:2]`` → empty list, because 3 > 2.
        """
        rows = self.ex.select(self.t, limit=2, offset=3)
        ids = [r["id"] for r in rows]
        self.assertEqual(ids, [4, 5])


# ═══════════════════════════════════════════════════════════════════
# INSERT
# ═══════════════════════════════════════════════════════════════════

class ExecutorInsertTest(unittest.TestCase):

    def setUp(self):
        self.ex = Executor()

    def test_insert_adds_row(self):
        t = Table("t", ["id", "name"], [])
        self.ex.insert(t, {"id": 1, "name": "alice"})
        self.assertEqual(len(t), 1)
        self.assertEqual(t.rows[0]["name"], "alice")

    def test_insert_returns_count(self):
        t = Table("t", ["id"], [])
        self.assertEqual(self.ex.insert(t, {"id": 1}), 1)


# ═══════════════════════════════════════════════════════════════════
# UPDATE
# ═══════════════════════════════════════════════════════════════════

class ExecutorUpdateTest(unittest.TestCase):

    def setUp(self):
        self.ex = Executor()

    def test_update_with_where(self):
        t = _people_table()
        count = self.ex.update(t, {"status": "banned"}, where=("name", "=", "bob"))
        self.assertEqual(count, 1)
        bob = [r for r in t.rows if r["name"] == "bob"][0]
        self.assertEqual(bob["status"], "banned")

    def test_update_all(self):
        t = _id_table(3)
        count = self.ex.update(t, {"id": 0})
        self.assertEqual(count, 3)
        self.assertTrue(all(r["id"] == 0 for r in t.rows))

    def test_update_returns_zero_when_no_match(self):
        t = _people_table()
        count = self.ex.update(t, {"status": "x"}, where=("name", "=", "nobody"))
        self.assertEqual(count, 0)


# ═══════════════════════════════════════════════════════════════════
# DELETE
# ═══════════════════════════════════════════════════════════════════

class ExecutorDeleteTest(unittest.TestCase):

    def setUp(self):
        self.ex = Executor()

    def test_delete_with_where(self):
        t = _people_table()
        count = self.ex.delete(t, where=("name", "=", "bob"))
        self.assertEqual(count, 1)
        self.assertEqual(len(t), 4)

    def test_delete_all(self):
        t = _id_table(3)
        count = self.ex.delete(t)
        self.assertEqual(count, 3)
        self.assertEqual(len(t), 0)

    def test_delete_returns_zero_when_no_match(self):
        t = _people_table()
        count = self.ex.delete(t, where=("name", "=", "nobody"))
        self.assertEqual(count, 0)
        self.assertEqual(len(t), 5)


# ═══════════════════════════════════════════════════════════════════
# AGGREGATE
# ═══════════════════════════════════════════════════════════════════

class ExecutorAggregateTest(unittest.TestCase):
    """Aggregate functions — 1 test FAILS due to Bug E3."""

    def setUp(self):
        self.ex = Executor()
        self.t = Table("scores", ["id", "name", "score"], [
            {"id": 1, "name": "alice", "score": 90},
            {"id": 2, "name": "bob",   "score": 80},
            {"id": 3, "name": "carol", "score": None},
            {"id": 4, "name": "dave",  "score": 70},
        ])

    def test_count_star(self):
        """COUNT(*) counts all rows, including NULLs."""
        self.assertEqual(self.ex.aggregate(self.t, "COUNT", "*"), 4)

    # ── FAILING: Bug E3 ──────────────────────────────────────────

    def test_count_column_skips_nulls(self):
        """COUNT(score) should not count rows where score is NULL.

        BUG E3: returns 4 (same as COUNT(*)) instead of 3,
        because the code doesn't filter out NULL values.
        """
        result = self.ex.aggregate(self.t, "COUNT", "score")
        self.assertEqual(result, 3)

    # ── PASSING ───────────────────────────────────────────────────

    def test_sum(self):
        self.assertEqual(self.ex.aggregate(self.t, "SUM", "score"), 240)

    def test_avg(self):
        self.assertEqual(self.ex.aggregate(self.t, "AVG", "score"), 80.0)

    def test_min(self):
        self.assertEqual(self.ex.aggregate(self.t, "MIN", "score"), 70)

    def test_max(self):
        self.assertEqual(self.ex.aggregate(self.t, "MAX", "score"), 90)

    def test_count_star_with_where(self):
        result = self.ex.aggregate(self.t, "COUNT", "*", where=("score", ">", 75))
        self.assertEqual(result, 2)

    def test_sum_with_where(self):
        result = self.ex.aggregate(self.t, "SUM", "score", where=("score", ">", 75))
        self.assertEqual(result, 170)

    def test_aggregate_empty_result(self):
        """SUM over no matching rows returns None."""
        result = self.ex.aggregate(self.t, "SUM", "score", where=("score", ">", 999))
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
