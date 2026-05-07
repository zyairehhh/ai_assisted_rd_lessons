"""Tests for the Mini SQL lexer.

Baseline: 2 FAIL  (LexerStringTest)  /  7 PASS  (LexerBasicsTest + others)
"""
import unittest

from minisql.lexer import Lexer, Token, LexError


class LexerBasicsTest(unittest.TestCase):
    """Basic tokenisation — all these tests should pass."""

    def setUp(self):
        self.lex = Lexer()

    def test_select_keywords(self):
        tokens = self.lex.tokenize("SELECT a FROM t")
        self.assertEqual(tokens[0], Token("KEYWORD", "SELECT"))
        self.assertEqual(tokens[1], Token("IDENTIFIER", "a"))
        self.assertEqual(tokens[2], Token("KEYWORD", "FROM"))
        self.assertEqual(tokens[3], Token("IDENTIFIER", "t"))

    def test_integer(self):
        tokens = self.lex.tokenize("42")
        self.assertEqual(tokens, [Token("INTEGER", 42)])

    def test_negative_integer(self):
        tokens = self.lex.tokenize("-7")
        self.assertEqual(tokens, [Token("INTEGER", -7)])

    def test_float(self):
        tokens = self.lex.tokenize("3.14")
        self.assertEqual(tokens, [Token("FLOAT", 3.14)])

    def test_operators(self):
        tokens = self.lex.tokenize("a >= 10")
        self.assertEqual(tokens[1], Token("SYMBOL", ">="))

    def test_two_char_not_equal(self):
        tokens = self.lex.tokenize("a != 1")
        self.assertEqual(tokens[1], Token("SYMBOL", "!="))

    def test_simple_string(self):
        tokens = self.lex.tokenize("'hello'")
        self.assertEqual(tokens, [Token("STRING", "hello")])

    def test_keywords_case_insensitive(self):
        tokens = self.lex.tokenize("select from where")
        kinds = [t.kind for t in tokens]
        self.assertEqual(kinds, ["KEYWORD", "KEYWORD", "KEYWORD"])

    def test_symbols(self):
        tokens = self.lex.tokenize("( ) , * =")
        values = [t.value for t in tokens]
        self.assertEqual(values, ["(", ")", ",", "*", "="])

    def test_null_keyword(self):
        tokens = self.lex.tokenize("NULL")
        self.assertEqual(tokens, [Token("KEYWORD", "NULL")])


class LexerStringTest(unittest.TestCase):
    """String literal edge cases — 2 of these tests FAIL due to bugs."""

    def setUp(self):
        self.lex = Lexer()

    # ── FAILING: Bug T1 ──────────────────────────────────────────

    def test_string_with_space(self):
        """'John Doe' should tokenise as a single STRING token.

        BUG T1: _split breaks on the space, producing fragments
        that _classify cannot recognise → LexError.
        """
        tokens = self.lex.tokenize("'John Doe'")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0], Token("STRING", "John Doe"))

    # ── FAILING: Bug T3 ──────────────────────────────────────────

    def test_digit_string_type(self):
        """'123' is a STRING whose value is the text "123", not an int.

        BUG T3: _classify sees all-digit content inside quotes and
        returns Token('INTEGER', 123) instead of Token('STRING', '123').
        """
        tokens = self.lex.tokenize("'123'")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].kind, "STRING")
        self.assertEqual(tokens[0].value, "123")

    # ── PASSING ───────────────────────────────────────────────────

    def test_string_preserves_content(self):
        tokens = self.lex.tokenize("'abc'")
        self.assertEqual(tokens[0], Token("STRING", "abc"))

    def test_empty_string(self):
        tokens = self.lex.tokenize("''")
        self.assertEqual(tokens[0], Token("STRING", ""))


if __name__ == "__main__":
    unittest.main()
