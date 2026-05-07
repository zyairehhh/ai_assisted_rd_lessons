"""Snapshot persistence: dump the ``kv`` table to a JSON file and restore it.

Although SQLite already gives us durable storage, operations teams still ask
for a portable text snapshot — for backup transfer, audit, or replay into a
different SQLite file. ``Snapshot.dump`` reads from the table and writes JSON;
``Snapshot.load`` truncates and re-inserts.

On-disk format::

    {
        "records": [
            {"key": "...", "value": "...", "expires_at": <unix_ts | null>},
            ...
        ]
    }
"""

from __future__ import annotations

import json

from .store import KVStore


class Snapshot:
    @staticmethod
    def dump(store: KVStore, path: str) -> None:
        rows = store._conn.execute(
            "SELECT key, value, expires_at FROM kv"
        ).fetchall()
        records = [
            {"key": k, "value": v, "expires_at": e} for k, v, e in rows
        ]
        with open(path, "w") as f:
            json.dump({"records": records}, f)

    @staticmethod
    def load(store: KVStore, path: str) -> None:
        with open(path) as f:
            payload = json.load(f)
        records = payload.get("records", [])
        store._conn.execute("DELETE FROM kv")
        for r in records:
            store._conn.execute(
                "INSERT INTO kv (key, value, expires_at) VALUES (?, ?, ?)",
                (r["key"], r["value"], r.get("expires_at")),
            )
