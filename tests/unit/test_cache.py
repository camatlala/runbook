from runbook.context.cache import ContextCache

def test_cache_stores_and_detects_changes():
    cache = ContextCache()
    assert cache.get("a.py") is None
    h1 = cache.put("a.py", "print(1)")
    assert cache.get("a.py") == "print(1)"
    assert cache.has_changed("a.py", "print(1)") is False
    assert cache.has_changed("a.py", "print(2)") is True
    h2 = cache.put("a.py", "print(2)")
    assert h1 != h2

def test_hash_of_is_stable():
    cache = ContextCache()
    assert cache.hash_of("same") == cache.hash_of("same")
    assert cache.hash_of("same") != cache.hash_of("different")
