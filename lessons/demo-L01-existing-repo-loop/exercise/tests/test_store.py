import time
import unittest

from kvstore.store import KVStore


class StoreBasicsTest(unittest.TestCase):
    def test_set_get(self):
        s = KVStore()
        s.set("a", "1")
        self.assertEqual("1", s.get("a"))

    def test_get_missing_returns_none(self):
        s = KVStore()
        self.assertIsNone(s.get("missing"))

    def test_overwrite(self):
        s = KVStore()
        s.set("a", "1")
        s.set("a", "2")
        self.assertEqual("2", s.get("a"))

    def test_delete_existing(self):
        s = KVStore()
        s.set("a", "1")
        self.assertTrue(s.delete("a"))
        self.assertIsNone(s.get("a"))

    def test_delete_missing(self):
        s = KVStore()
        self.assertFalse(s.delete("missing"))

    def test_keys_lists_all_set(self):
        s = KVStore()
        s.set("a", "1")
        s.set("b", "2")
        self.assertEqual(["a", "b"], sorted(s.keys()))

    def test_len_counts_set(self):
        s = KVStore()
        s.set("a", "1")
        s.set("b", "2")
        self.assertEqual(2, len(s))

    def test_contains_for_existing(self):
        s = KVStore()
        s.set("a", "1")
        self.assertIn("a", s)
        self.assertNotIn("b", s)


class StoreTtlTest(unittest.TestCase):
    def test_set_with_ttl_get_returns_none_after_expiry(self):
        s = KVStore()
        s.set("a", "1", ex=0.05)
        self.assertEqual("1", s.get("a"))
        time.sleep(0.1)
        self.assertIsNone(s.get("a"))

    def test_overwrite_clears_ttl(self):
        s = KVStore()
        s.set("a", "1", ex=0.05)
        s.set("a", "2")
        time.sleep(0.1)
        self.assertEqual("2", s.get("a"))

    def test_expire_existing_key(self):
        s = KVStore()
        s.set("a", "1")
        self.assertTrue(s.expire("a", 0.05))
        time.sleep(0.1)
        self.assertIsNone(s.get("a"))

    def test_expire_missing_key_returns_false(self):
        s = KVStore()
        self.assertFalse(s.expire("missing", 1.0))

    def test_ttl_no_expiry_set(self):
        s = KVStore()
        s.set("a", "1")
        self.assertEqual(-1.0, s.ttl("a"))

    def test_ttl_missing_key(self):
        s = KVStore()
        self.assertIsNone(s.ttl("missing"))

    def test_ttl_after_expiry(self):
        s = KVStore()
        s.set("a", "1", ex=0.05)
        time.sleep(0.1)
        self.assertIsNone(s.ttl("a"))


class StoreExpirationViewTest(unittest.TestCase):
    """Tests that expose the集合视图 bug. Fail on baseline; pass after fix."""

    def test_keys_excludes_expired(self):
        s = KVStore()
        s.set("a", "1", ex=0.05)
        s.set("b", "2")
        time.sleep(0.1)
        self.assertEqual(["b"], sorted(s.keys()))

    def test_len_excludes_expired(self):
        s = KVStore()
        s.set("a", "1", ex=0.05)
        s.set("b", "2")
        time.sleep(0.1)
        self.assertEqual(1, len(s))

    def test_contains_returns_false_for_expired(self):
        s = KVStore()
        s.set("a", "1", ex=0.05)
        time.sleep(0.1)
        self.assertNotIn("a", s)


class StoreDeleteSemanticsTest(unittest.TestCase):
    """delete() should mirror expire()'s expiration handling: an expired key
    is logically gone, so deleting it should report False."""

    def test_delete_on_expired_key_returns_false(self):
        s = KVStore()
        s.set("a", "1", ex=0.05)
        time.sleep(0.1)
        self.assertFalse(s.delete("a"))

    def test_delete_on_live_key_still_returns_true(self):
        s = KVStore()
        s.set("a", "1", ex=5)
        self.assertTrue(s.delete("a"))


if __name__ == "__main__":
    unittest.main()
