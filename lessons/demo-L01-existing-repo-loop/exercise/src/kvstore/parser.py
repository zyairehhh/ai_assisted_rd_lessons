"""Tiny command parser. Supports SET / GET / DEL / EXPIRE / TTL / KEYS."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


class ParseError(ValueError):
    pass


@dataclass(frozen=True)
class Command:
    op: str
    key: Optional[str] = None
    value: Optional[str] = None
    ttl: Optional[float] = None


def parse(line: str) -> Command:
    tokens = line.strip().split()
    if not tokens:
        raise ParseError("empty command")
    op = tokens[0].upper()

    if op == "SET":
        if len(tokens) < 3:
            raise ParseError("SET requires key and value")
        key, value = tokens[1], tokens[2]
        ttl: Optional[float] = None
        if len(tokens) == 3:
            pass  # SET key value
        elif len(tokens) == 5 and tokens[3].upper() == "EX":
            ttl = _parse_float(tokens[4], "TTL")
        else:
            raise ParseError("invalid SET syntax")
        return Command(op="SET", key=key, value=value, ttl=ttl)

    if op == "GET":
        _require_argc(tokens, 2, "GET")
        return Command(op="GET", key=tokens[1])

    if op == "DEL":
        _require_argc(tokens, 2, "DEL")
        return Command(op="DEL", key=tokens[1])

    if op == "EXPIRE":
        _require_argc(tokens, 3, "EXPIRE")
        return Command(op="EXPIRE", key=tokens[1], ttl=_parse_float(tokens[2], "TTL"))

    if op == "TTL":
        _require_argc(tokens, 2, "TTL")
        return Command(op="TTL", key=tokens[1])

    if op == "KEYS":
        _require_argc(tokens, 1, "KEYS")
        return Command(op="KEYS")

    raise ParseError(f"unknown command: {op}")


def _require_argc(tokens: list[str], n: int, name: str) -> None:
    if len(tokens) != n:
        raise ParseError(f"{name} expects {n - 1} argument(s), got {len(tokens) - 1}")


def _parse_float(s: str, label: str) -> float:
    try:
        return float(s)
    except ValueError as e:
        raise ParseError(f"invalid {label}: {s}") from e
