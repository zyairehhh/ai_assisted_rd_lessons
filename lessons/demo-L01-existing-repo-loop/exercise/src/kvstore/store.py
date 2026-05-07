"""SQLite-backed KV store with lazy TTL expiration.

The store persists rows in a single ``kv`` table::

    CREATE TABLE kv (
        key        TEXT PRIMARY KEY,
        value      TEXT NOT NULL,
        expires_at REAL              -- NULL means no TTL; otherwise absolute Unix time
    )

TTL semantics are unchanged from the in-memory variant: ``get()`` and ``ttl()``
clean up rows lazily when they observe expiration. Other access paths must
honor the same rule by adding a ``WHERE`` filter on ``expires_at``.
"""

from __future__ import annotations

import sqlite3
import time
from typing import Optional


SCHEMA = """
CREATE TABLE IF NOT EXISTS kv (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    expires_at REAL
)
"""


class KVStore:
    def __init__(self, path: str = ":memory:") -> None:
        # isolation_level=None puts sqlite3 into autocommit mode; every
        # statement commits immediately. Keeps the training code simple.
        self._conn = sqlite3.connect(path, isolation_level=None)
        self._conn.execute(SCHEMA)

    def close(self) -> None:
        self._conn.close()

    def set(self, key: str, value: str, ex: Optional[float] = None) -> None:
        expires_at = time.time() + ex if ex is not None else None
        self._conn.execute(
            "INSERT INTO kv (key, value, expires_at) VALUES (?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET "
            "    value = excluded.value, "
            "    expires_at = excluded.expires_at",
            (key, value, expires_at),
        )

    def get(self, key: str) -> Optional[str]:
        row = self._conn.execute(
            "SELECT value, expires_at FROM kv WHERE key = ?",
            (key,),
        ).fetchone()
        if row is None:
            return None
        value, expires_at = row
        if expires_at is not None and time.time() >= expires_at:
            self._evict(key)
            return None
        return value

    def delete(self, key: str) -> bool:
        cur = self._conn.execute("DELETE FROM kv WHERE key = ?", (key,))
        return cur.rowcount > 0

    def expire(self, key: str, ex: float) -> bool:
        row = self._conn.execute(
            "SELECT expires_at FROM kv WHERE key = ?", (key,)
        ).fetchone()
        if row is None:
            return False
        expires_at = row[0]
        if expires_at is not None and time.time() >= expires_at:
            self._evict(key)
            return False
        self._conn.execute(
            "UPDATE kv SET expires_at = ? WHERE key = ?",
            (time.time() + ex, key),
        )
        return True

    def ttl(self, key: str) -> Optional[float]:
        row = self._conn.execute(
            "SELECT expires_at FROM kv WHERE key = ?", (key,)
        ).fetchone()
        if row is None:
            return None
        expires_at = row[0]
        if expires_at is None:
            return -1.0
        if time.time() >= expires_at:
            self._evict(key)
            return None
        return expires_at - time.time()

    def keys(self) -> list[str]:
        rows = self._conn.execute("SELECT key FROM kv").fetchall()
        return [row[0] for row in rows]

    def __len__(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM kv").fetchone()[0]

    def __contains__(self, key: str) -> bool:
        return (
            self._conn.execute(
                "SELECT 1 FROM kv WHERE key = ?", (key,)
            ).fetchone()
            is not None
        )

    def _evict(self, key: str) -> None:
        self._conn.execute("DELETE FROM kv WHERE key = ?", (key,))
