import re


class QueryError(ValueError):
    """Raised when MiniDB cannot parse or execute a query."""


class MiniDB:
    def __init__(self):
        self.tables = {
            "employees": [
                {"id": 1, "name": "Ada", "age": 34, "dept": "db"},
                {"id": 2, "name": "Linus", "age": 29, "dept": "kernel"},
                {"id": 3, "name": "Grace", "age": 41, "dept": "db"},
                {"id": 4, "name": "Edsger", "age": 38, "dept": "compiler"},
            ]
        }

    def execute(self, sql):
        query = parse_select(sql)
        rows = list(self._table(query["table"]))

        if query["where"] is not None:
            rows = [row for row in rows if matches_where(row, query["where"])]

        limit = query["limit"]
        if limit:
            rows = rows[:limit]

        return rows

    def _table(self, name):
        try:
            return self.tables[name]
        except KeyError as exc:
            raise QueryError(f"unknown table: {name}") from exc


def parse_select(sql):
    pattern = re.compile(
        r"^\s*select\s+\*\s+from\s+"
        r"(?P<table>[a-zA-Z_][a-zA-Z0-9_]*)"
        r"(?:\s+where\s+(?P<where>.+?))?"
        r"(?:\s+limit\s+(?P<limit>-?\d+))?"
        r"\s*;?\s*$",
        re.IGNORECASE,
    )
    match = pattern.match(sql)
    if not match:
        raise QueryError(f"unsupported query: {sql}")

    limit_text = match.group("limit")
    limit = None if limit_text is None else int(limit_text)
    if limit is not None and limit < 0:
        raise QueryError("LIMIT must be non-negative")

    return {
        "table": match.group("table").lower(),
        "where": parse_where(match.group("where")),
        "limit": limit,
    }


def parse_where(where_text):
    if where_text is None:
        return None

    match = re.match(
        r"^\s*(?P<column>[a-zA-Z_][a-zA-Z0-9_]*)\s*"
        r"(?P<op>=|>|<)\s*"
        r"(?P<value>'[^']*'|\d+)\s*$",
        where_text,
        re.IGNORECASE,
    )
    if not match:
        raise QueryError(f"unsupported WHERE clause: {where_text}")

    raw_value = match.group("value")
    if raw_value.startswith("'") and raw_value.endswith("'"):
        value = raw_value[1:-1]
    else:
        value = int(raw_value)

    return {
        "column": match.group("column").lower(),
        "op": match.group("op"),
        "value": value,
    }


def matches_where(row, condition):
    column = condition["column"]
    if column not in row:
        raise QueryError(f"unknown column: {column}")

    left = row[column]
    right = condition["value"]
    op = condition["op"]

    if op == "=":
        return left == right
    if op == ">":
        return left > right
    if op == "<":
        return left < right

    raise QueryError(f"unsupported operator: {op}")
