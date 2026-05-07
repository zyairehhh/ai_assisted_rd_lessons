import json
import os
import tempfile
import time
import unittest

from kvstore.persistence import Snapshot
from kvstore.store import KVStore


class SnapshotTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.path = os.path.join(self.tmpdir, "snap.json")

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)
        os.rmdir(self.tmpdir)

    def test_dump_and_load_roundtrip(self):
        s1 = KVStore()
        s1.set("a", "1")
        s1.set("b", "2")
        Snapshot.dump(s1, self.path)
        s2 = KVStore()
        Snapshot.load(s2, self.path)
        self.assertEqual("1", s2.get("a"))
        self.assertEqual("2", s2.get("b"))

    def test_dump_preserves_ttl(self):
        s1 = KVStore()
        s1.set("a", "1", ex=5)
        Snapshot.dump(s1, self.path)
        s2 = KVStore()
        Snapshot.load(s2, self.path)
        ttl = s2.ttl("a")
        self.assertIsNotNone(ttl)
        self.assertGreater(ttl, 0)
        self.assertLessEqual(ttl, 5)

    def test_load_replaces_existing_state(self):
        s = KVStore()
        s.set("old", "1")
        snap = {"records": [{"key": "new", "value": "2", "expires_at": None}]}
        with open(self.path, "w") as f:
            json.dump(snap, f)
        Snapshot.load(s, self.path)
        self.assertEqual("2", s.get("new"))
        self.assertIsNone(s.get("old"))

    def test_load_resurrects_expired_keys_lazily(self):
        """Snapshot stores absolute expiry; expired keys appear gone after load."""
        s1 = KVStore()
        s1.set("ghost", "x", ex=0.05)
        time.sleep(0.1)
        Snapshot.dump(s1, self.path)
        s2 = KVStore()
        Snapshot.load(s2, self.path)
        self.assertIsNone(s2.get("ghost"))

    def test_dump_excludes_expired_keys(self):
        """Snapshot must not persist already-expired keys.

        Persisting them bloats the file and surfaces dead data through any
        path that hasn't applied lazy expiration. The on-disk view should
        match the live view.
        """
        s = KVStore()
        s.set("alive", "1")
        s.set("dying", "2", ex=0.05)
        time.sleep(0.1)
        Snapshot.dump(s, self.path)
        with open(self.path) as f:
            snap = json.load(f)
        keys_in_snapshot = {r["key"] for r in snap["records"]}
        self.assertEqual({"alive"}, keys_in_snapshot)


if __name__ == "__main__":
    unittest.main()
