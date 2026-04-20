import unittest

from minidb import MiniDB, QueryError


class MiniDBTest(unittest.TestCase):
    def setUp(self):
        self.db = MiniDB()

    def test_select_all(self):
        rows = self.db.execute("SELECT * FROM employees;")
        self.assertEqual(4, len(rows))

    def test_where_greater_than(self):
        rows = self.db.execute("SELECT * FROM employees WHERE age > 35;")
        self.assertEqual(["Grace", "Edsger"], [row["name"] for row in rows])

    def test_where_equals_string(self):
        rows = self.db.execute("SELECT * FROM employees WHERE dept = 'db';")
        self.assertEqual(["Ada", "Grace"], [row["name"] for row in rows])

    def test_limit_positive(self):
        rows = self.db.execute("SELECT * FROM employees LIMIT 2;")
        self.assertEqual(["Ada", "Linus"], [row["name"] for row in rows])

    def test_limit_zero_returns_empty_result(self):
        rows = self.db.execute("SELECT * FROM employees LIMIT 0;")
        self.assertEqual([], rows)

    def test_limit_with_where(self):
        rows = self.db.execute("SELECT * FROM employees WHERE age > 30 LIMIT 1;")
        self.assertEqual(["Ada"], [row["name"] for row in rows])

    def test_negative_limit_is_rejected(self):
        with self.assertRaises(QueryError):
            self.db.execute("SELECT * FROM employees LIMIT -1;")


if __name__ == "__main__":
    unittest.main()
