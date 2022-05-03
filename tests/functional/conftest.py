import asyncio
import json
from dataclasses import dataclass
from typing import Optional

import aiohttp
import aioredis
import pytest
from functional.config import DatabaseConfig, TestFilesPath
from functional.models.new_base_model import NewBaseModel
from functional.settings import TestSettings
from multidict import CIMultiDictProxy

settings = TestSettings()
db_config = DatabaseConfig()
test_data = TestFilesPath()


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


class CacheService:
    def __init__(self, cache: aioredis.Redis):
        self.cache = cache

    async def get(self, index, key=None, model=NewBaseModel):
        data = await self.cache.get(f"{index}: {key}" if key else index)
        if not data:
            return None
        if isinstance(data := json.loads(data), list):
            data = [json.loads(item) for item in data]
            return [model(**film) for film in data]
        else:
            return model.parse_obj(data)


@pytest.fixture(scope="session")
async def cache_client():
    client = await aioredis.create_redis_pool((settings.redis_host, settings.redis_port), minsize=10, maxsize=20)
    yield CacheService(client)
    await client.flushdb()
    client.close()

@pytest.fixture(scope="session")
def db_conn():
    return db_config.ENGINE.connect()

@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(url: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner

@pytest.fixture
def make_post_request(session):
    async def inner(url: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        async with session.post(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
