from pydantic import TypeAdapter
from pydantic.json import pydantic_encoder
from redis.asyncio import Redis
from functools import wraps
import pickle

redis_client: Redis = None  

async def init_redis():
    global redis_client 
    redis_client = Redis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=False)

def get_redis_client() -> Redis:
    global redis_client
    return redis_client

def cache(key: str = "", key_args: bool = True, expire: int = 0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            global redis_client
            nonlocal func, key, expire, key_args
            
            unique_key = str(id(func))
            if key:
                unique_key = key
            if key_args:
                unique_key = f"{unique_key}:{args}:{kwargs}"

            data = await redis_client.get(unique_key)
            if data:
                try:
                    return pickle.loads(data)
                except Exception as e:
                    print(e)
            
            result = await func(*args, **kwargs)
            
            if expire > 0:
                await redis_client.setex(unique_key, expire, pickle.dumps(result))
            else:
                await redis_client.set(unique_key, pickle.dumps(result))

            return result
        return wrapper
    return decorator
