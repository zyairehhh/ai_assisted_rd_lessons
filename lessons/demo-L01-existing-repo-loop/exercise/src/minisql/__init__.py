"""Mini SQL — a toy SQL lexer / parser / formatter for teaching purposes."""

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
from .formatter import Formatter
from .lexer import Lexer, LexError, Token
from .parser import Parser, ParseError


def parse(sql: str) -> Statement:
    """Convenience: lex + parse in one call."""
    tokens = Lexer().tokenize(sql)
    return Parser(tokens).parse()


def format_sql(stmt: Statement) -> str:
    """Convenience: format an AST back to SQL."""
    return Formatter().format(stmt)
