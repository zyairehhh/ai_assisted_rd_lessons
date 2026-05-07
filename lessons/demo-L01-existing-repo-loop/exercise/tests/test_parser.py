import unittest

from kvstore.parser import Command, ParseError, parse


class ParserTest(unittest.TestCase):
    def test_set_basic(self):
        self.assertEqual(
            Command(op="SET", key="a", value="1", ttl=None),
            parse("SET a 1"),
        )

    def test_set_with_ttl(self):
        self.assertEqual(
            Command(op="SET", key="a", value="1", ttl=5.0),
            parse("SET a 1 EX 5"),
        )

    def test_get(self):
        self.assertEqual(Command(op="GET", key="a"), parse("GET a"))

    def test_del(self):
        self.assertEqual(Command(op="DEL", key="a"), parse("DEL a"))

    def test_expire(self):
        self.assertEqual(Command(op="EXPIRE", key="a", ttl=10.0), parse("EXPIRE a 10"))

    def test_ttl(self):
        self.assertEqual(Command(op="TTL", key="a"), parse("TTL a"))

    def test_keys(self):
        self.assertEqual(Command(op="KEYS"), parse("KEYS"))

    def test_lowercase_op_normalized(self):
        self.assertEqual("GET", parse("get a").op)

    def test_empty_raises(self):
        with self.assertRaises(ParseError):
            parse("")

    def test_unknown_op_raises(self):
        with self.assertRaises(ParseError):
            parse("FOOBAR x")

    def test_set_missing_value_raises(self):
        with self.assertRaises(ParseError):
            parse("SET a")

    def test_get_too_many_args_raises(self):
        with self.assertRaises(ParseError):
            parse("GET a b")

    def test_invalid_ttl_raises(self):
        with self.assertRaises(ParseError):
            parse("EXPIRE a notanumber")

    def test_set_rejects_trailing_garbage(self):
        with self.assertRaises(ParseError):
            parse("SET a 1 EX 5 garbage")


if __name__ == "__main__":
    unittest.main()
