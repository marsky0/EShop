from redis.asyncio import Redis

from app.core.config import settings

redis_client: Redis = None  

async def init_redis():
    global redis_client
    redis_client = Redis.from_url(settings.redis_url, encoding="utf-8", decode_responses=False)

def get_redis_client() -> Redis:
    global redis_client
    return redis_client
