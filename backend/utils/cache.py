import time
import threading
import re
from typing import Any, Callable, Dict, List, Optional, Tuple
from functools import wraps
import asyncio
from utils.logger import Logger

log = Logger().get_logger()


class CacheEntry:
    __slots__ = ("value", "expires_at", "last_accessed")

    def __init__(self, value: Any, ttl_seconds: float):
        now = time.time()
        self.value = value
        self.expires_at = (now + ttl_seconds) if ttl_seconds > 0 else float("inf")
        self.last_accessed = now

    def is_expired(self, now: float) -> bool:
        return now > self.expires_at


class TTLCache:
    """
    Thread-safe, high-performance in-memory cache with:
    - Time-to-live (TTL) expiration per item
    - Least-Recently-Used (LRU) bounded memory eviction
    - Pattern and prefix invalidation
    - Hit/miss telemetry statistics
    """

    def __init__(self, default_ttl: int = 300, max_size: int = 2000):
        self.default_ttl = default_ttl
        self.max_size = max_size
        self._store: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0
        self._evictions = 0

    def get(self, key: str) -> Optional[Any]:
        now = time.time()
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                self._misses += 1
                return None

            if entry.is_expired(now):
                del self._store[key]
                self._misses += 1
                return None

            entry.last_accessed = now
            self._hits += 1
            return entry.value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ttl_val = float(ttl if ttl is not None else self.default_ttl)
        now = time.time()

        with self._lock:
            # If at max size, evict expired entries first
            if len(self._store) >= self.max_size and key not in self._store:
                self._evict_lru_or_expired(now)

            self._store[key] = CacheEntry(value, ttl_val)

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    def invalidate_prefix(self, prefix: str) -> int:
        """Removes all keys starting with the given prefix."""
        with self._lock:
            keys_to_del = [k for k in self._store if k.startswith(prefix)]
            for k in keys_to_del:
                del self._store[k]
            if keys_to_del:
                log.info(f"Invalidated {len(keys_to_del)} cache keys with prefix '{prefix}'.")
            return len(keys_to_del)

    def invalidate_pattern(self, pattern: str) -> int:
        """Removes all keys matching a regex pattern."""
        regex = re.compile(pattern)
        with self._lock:
            keys_to_del = [k for k in self._store if regex.search(k)]
            for k in keys_to_del:
                del self._store[k]
            if keys_to_del:
                log.info(f"Invalidated {len(keys_to_del)} cache keys matching pattern '{pattern}'.")
            return len(keys_to_del)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()
            log.info("Cache completely cleared.")

    def _evict_lru_or_expired(self, now: float) -> None:
        # First pass: clean expired items
        expired = [k for k, v in self._store.items() if v.is_expired(now)]
        if expired:
            for k in expired:
                del self._store[k]
            self._evictions += len(expired)
            return

        # Second pass: evict 10% least recently accessed items
        if not self._store:
            return

        sorted_keys = sorted(self._store.keys(), key=lambda k: self._store[k].last_accessed)
        to_evict = max(1, len(sorted_keys) // 10)
        for k in sorted_keys[:to_evict]:
            del self._store[k]
            self._evictions += 1

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            now = time.time()
            active_keys = [k for k, v in self._store.items() if not v.is_expired(now)]
            total_requests = self._hits + self._misses
            hit_rate = (self._hits / total_requests) if total_requests > 0 else 0.0

            return {
                "active_items": len(active_keys),
                "total_stored_items": len(self._store),
                "max_size": self.max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate_pct": round(hit_rate * 100, 2),
                "evictions": self._evictions,
                "sample_keys": active_keys[:20],
            }


# Global singleton cache instance
backend_cache = TTLCache(default_ttl=300, max_size=2000)


def cached(
    ttl: Optional[int] = None,
    prefix: str = "cache",
    key_builder: Optional[Callable[..., str]] = None,
):
    """
    Decorator for caching function/method return values.
    Supports both async and synchronous functions.
    """
    def decorator(fn: Callable):
        @wraps(fn)
        async def async_wrapper(*args, **kwargs):
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                args_str = ":".join(str(a) for a in args)
                kwargs_str = ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
                cache_key = f"{prefix}:{fn.__name__}:{args_str}:{kwargs_str}"

            cached_val = backend_cache.get(cache_key)
            if cached_val is not None:
                return cached_val

            result = await fn(*args, **kwargs)
            if result is not None:
                backend_cache.set(cache_key, result, ttl=ttl)
            return result

        @wraps(fn)
        def sync_wrapper(*args, **kwargs):
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                args_str = ":".join(str(a) for a in args)
                kwargs_str = ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
                cache_key = f"{prefix}:{fn.__name__}:{args_str}:{kwargs_str}"

            cached_val = backend_cache.get(cache_key)
            if cached_val is not None:
                return cached_val

            result = fn(*args, **kwargs)
            if result is not None:
                backend_cache.set(cache_key, result, ttl=ttl)
            return result

        if asyncio.iscoroutinefunction(fn):
            return async_wrapper
        return sync_wrapper

    return decorator
