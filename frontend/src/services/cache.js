/**
 * Client-Side Caching Service
 * 
 * Provides:
 * - Ultra-fast in-memory LRU cache (0ms lookup)
 * - Optional SessionStorage persistence for static resources (chunks/transcripts)
 * - Configurable TTL per resource type
 * - Pattern-based and prefix-based cache invalidation
 * - Stale-While-Revalidate support for instant UI rendering
 */

const STORAGE_PREFIX = 'ms_cache_';

// Default TTLs in milliseconds
export const CACHE_TTL = {
  MEETINGS: 3 * 60 * 1000,      // 3 minutes
  CHUNKS: 30 * 60 * 1000,       // 30 minutes (chunks are immutable)
  OUTPUTS: 15 * 60 * 1000,      // 15 minutes
  ACTION_ITEMS: 60 * 1000,      // 1 minute (frequently modified)
  PROFILE: 10 * 60 * 1000,      // 10 minutes
  CHAT: 15 * 60 * 1000,         // 15 minutes
  DEFAULT: 5 * 60 * 1000,       // 5 minutes
};

class ClientCache {
  constructor(maxMemoryItems = 500) {
    this.memoryStore = new Map();
    this.maxMemoryItems = maxMemoryItems;
    this._hits = 0;
    this._misses = 0;
  }

  /**
   * Retrieves an item from memory or sessionStorage if not expired.
   */
  get(key) {
    const now = Date.now();

    // 1. Check in-memory Map
    if (this.memoryStore.has(key)) {
      const entry = this.memoryStore.get(key);
      if (now <= entry.expiresAt) {
        this._hits += 1;
        // Move to end for LRU refresh
        this.memoryStore.delete(key);
        this.memoryStore.set(key, entry);
        return entry.value;
      }
      // Expired
      this.memoryStore.delete(key);
    }

    // 2. Check SessionStorage fallback
    try {
      const storageKey = STORAGE_PREFIX + key;
      const raw = sessionStorage.getItem(storageKey);
      if (raw) {
        const entry = JSON.parse(raw);
        if (now <= entry.expiresAt) {
          this._hits += 1;
          // Hydrate memory cache
          this.setMemory(key, entry.value, entry.expiresAt);
          return entry.value;
        }
        sessionStorage.removeItem(storageKey);
      }
    } catch {
      // SessionStorage might be disabled or unavailable
    }

    this._misses += 1;
    return null;
  }

  /**
   * Stores an item with a TTL.
   */
  set(key, value, ttlMs = CACHE_TTL.DEFAULT, persist = false) {
    const expiresAt = Date.now() + (ttlMs || CACHE_TTL.DEFAULT);

    this.setMemory(key, value, expiresAt);

    if (persist) {
      try {
        const storageKey = STORAGE_PREFIX + key;
        sessionStorage.setItem(
          storageKey,
          JSON.stringify({ value, expiresAt })
        );
      } catch (e) {
        console.warn('SessionStorage cache quota or access notice:', e);
      }
    }
  }

  setMemory(key, value, expiresAt) {
    if (this.memoryStore.size >= this.maxMemoryItems && !this.memoryStore.has(key)) {
      // Evict oldest item (first key in map)
      const oldestKey = this.memoryStore.keys().next().value;
      if (oldestKey) this.memoryStore.delete(oldestKey);
    }
    this.memoryStore.set(key, { value, expiresAt });
  }

  /**
   * Removes a single key.
   */
  delete(key) {
    this.memoryStore.delete(key);
    try {
      sessionStorage.removeItem(STORAGE_PREFIX + key);
    } catch {}
  }

  /**
   * Invalidates all keys matching a prefix or regex pattern.
   */
  invalidate(patternOrPrefix) {
    let count = 0;
    const regex = patternOrPrefix instanceof RegExp ? patternOrPrefix : null;
    const prefix = typeof patternOrPrefix === 'string' ? patternOrPrefix : null;

    // Invalidate Memory
    for (const key of Array.from(this.memoryStore.keys())) {
      const match = regex ? regex.test(key) : (prefix ? key.startsWith(prefix) : false);
      if (match) {
        this.memoryStore.delete(key);
        count++;
      }
    }

    // Invalidate SessionStorage
    try {
      for (let i = sessionStorage.length - 1; i >= 0; i--) {
        const k = sessionStorage.key(i);
        if (k && k.startsWith(STORAGE_PREFIX)) {
          const rawKey = k.slice(STORAGE_PREFIX.length);
          const match = regex ? regex.test(rawKey) : (prefix ? rawKey.startsWith(prefix) : false);
          if (match) {
            sessionStorage.removeItem(k);
          }
        }
      }
    } catch {}

    return count;
  }

  /**
   * Clears the entire client cache.
   */
  clear() {
    this.memoryStore.clear();
    try {
      for (let i = sessionStorage.length - 1; i >= 0; i--) {
        const k = sessionStorage.key(i);
        if (k && k.startsWith(STORAGE_PREFIX)) {
          sessionStorage.removeItem(k);
        }
      }
    } catch {}
  }

  /**
   * High-level wrapper to wrap any async fetcher call with caching.
   */
  async fetchWithCache(key, fetcher, options = {}) {
    const {
      ttl = CACHE_TTL.DEFAULT,
      persist = false,
      forceRefresh = false,
      staleWhileRevalidate = false,
    } = options;

    if (!forceRefresh) {
      const cachedData = this.get(key);
      if (cachedData !== null) {
        if (staleWhileRevalidate) {
          // Trigger background update without awaiting
          fetcher()
            .then((fresh) => {
              if (fresh) this.set(key, fresh, ttl, persist);
            })
            .catch(() => {});
        }
        return cachedData;
      }
    }

    const freshData = await fetcher();
    if (freshData !== null && freshData !== undefined) {
      this.set(key, freshData, ttl, persist);
    }
    return freshData;
  }

  stats() {
    return {
      memoryEntries: this.memoryStore.size,
      hits: this._hits,
      misses: this._misses,
      hitRate: this._hits + this._misses > 0 
        ? ((this._hits / (this._hits + this._misses)) * 100).toFixed(1) + '%' 
        : '0%',
    };
  }
}

export const clientCache = new ClientCache();
