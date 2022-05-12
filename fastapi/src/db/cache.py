import json
from typing import Optional

import backoff
from aioredis import Redis, RedisError
from db.interfaces import CacheBase

cache: Optional[Redis] = None


async def get_cache() -> Redis:
    return cache


class CacheService(CacheBase):
    def __init__(self, cache: Redis):
        self.cache = cache

    @backoff.on_exception(backoff.expo, RedisError, max_time=10, factor=2)
    async def get(self, index, key=None):
        data = await self.cache.get(f'{index}: {key}' if key else index)
        if not data:
            return None
        if isinstance(data := json.loads(data), list):
            return [json.loads(item) for item in data]
        else:
            return data

    @backoff.on_exception(backoff.expo, RedisError, max_time=10, factor=2)
    async def set(self, key: str, value: str, expire: int) -> None:
        await self.cache.set(key=key, value=value, expire=expire)
