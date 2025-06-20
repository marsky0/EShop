from redis.asyncio import Redis

redis_client: Redis = None  

async def init_redis():
    global redis_client 
    redis_client = Redis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=False)

def get_redis_client() -> Redis:
    global redis_client
    return redis_client
