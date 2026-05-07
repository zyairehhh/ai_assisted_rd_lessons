"""Mini Query Executor — in-memory SQL-like query engine for teaching."""

from .evaluator import Condition, EvalError, Evaluator
from .executor import Executor
from .table import Row, Table
