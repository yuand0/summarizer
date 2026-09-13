import redis
import hashlib
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

redis_client = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2
)

# 命中率统计
cache_stats = {"hit": 0, "miss": 0}

def get_cache_key(text: str) -> str:
    return f"summary:{hashlib.sha256(text.encode()).hexdigest()}"

def get_cached_summary(text: str):
    try:
        key = get_cache_key(text)
        cached = redis_client.get(key)
        if cached:
            cache_stats["hit"] += 1
            total = cache_stats["hit"] + cache_stats["miss"]
            rate = cache_stats["hit"] / total * 100
            logger.info(f"[CACHE HIT] 命中率: {rate:.1f}% ({cache_stats['hit']}/{total})")
            return json.loads(cached)
        else:
            cache_stats["miss"] += 1
            total = cache_stats["hit"] + cache_stats["miss"]
            rate = cache_stats["hit"] / total * 100
            logger.info(f"[CACHE MISS] 命中率: {rate:.1f}% ({cache_stats['hit']}/{total})")
            return None
    except Exception as e:
        logger.error(f"Redis 读取失败: {e}")
        return None

def set_cached_summary(text: str, result: dict, ttl: int = 3600):
    try:
        key = get_cache_key(text)
        redis_client.setex(key, ttl, json.dumps(result))
    except Exception as e:
        logger.error(f"Redis 写入失败: {e}")

def get_cache_stats():
    """返回缓存命中率统计"""
    total = cache_stats["hit"] + cache_stats["miss"]
    rate = cache_stats["hit"] / total * 100 if total > 0 else 0
    return {
        "hit": cache_stats["hit"],
        "miss": cache_stats["miss"],
        "total": total,
        "hit_rate": f"{rate:.1f}%"
    }
