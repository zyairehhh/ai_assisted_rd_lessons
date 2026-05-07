"""Line-oriented CLI for the KV store. `python -m kvstore.cli`."""

from __future__ import annotations

import sys

from .parser import ParseError, parse
from .store import KVStore


def execute(store: KVStore, line: str) -> str:
    try:
        cmd = parse(line)
    except ParseError as e:
        return f"ERR {e}"

    if cmd.op == "SET":
        store.set(cmd.key, cmd.value, ex=cmd.ttl)
        return "OK"
    if cmd.op == "GET":
        v = store.get(cmd.key)
        return "(nil)" if v is None else str(v)
    if cmd.op == "DEL":
        return "1" if store.delete(cmd.key) else "0"
    if cmd.op == "EXPIRE":
        return "1" if store.expire(cmd.key, cmd.ttl) else "0"
    if cmd.op == "TTL":
        t = store.ttl(cmd.key)
        if t is None:
            return "(nil)"
        if t == -1.0:
            return "-1"
        return f"{t:.2f}"
    if cmd.op == "KEYS":
        ks = store.keys()
        return "\n".join(ks) if ks else "(empty)"
    return "ERR not implemented"


def main() -> None:
    store = KVStore()
    for line in sys.stdin:
        if not line.strip():
            continue
        print(execute(store, line))


if __name__ == "__main__":
    main()
