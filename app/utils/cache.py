from redis.asyncio import Redis
from functools import wraps
import pickle

from app.core.redis_client import get_redis_client

def cache(key: str = "", key_args: bool = True, expire: int = 0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis_client = get_redis_client()
            nonlocal func, key, expire, key_args
            
            unique_key = str(id(func))
            if key:
                unique_key = key
            if key_args:
                unique_key = f"cache:{unique_key}:{args}:{kwargs}"

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
