import time
from typing import Any

CACHE = {}
TTL = 60  # seconds

def get_cache(key: str) -> Any | None:
    data = CACHE.get(key)
    if not data:
        return None
    value, expiry = data
    if time.time() > expiry:
        CACHE.pop(key, None)
        return None
    return value

def set_cache(key: str, value: Any):
    CACHE[key] = (value, time.time() + TTL)
