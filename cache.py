import redis
import hashlib
import json
import os

redis_client = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

def get_cache_key(text: str) -> str:
    return f"summary:{hashlib.sha256(text.encode()).hexdigest()}"

def get_cached_summary(text: str):
    key = get_cache_key(text)
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    return None

def set_cached_summary(text: str, result: dict, ttl: int = 3600):
    key = get_cache_key(text)
    redis_client.setex(key, ttl, json.dumps(result))
