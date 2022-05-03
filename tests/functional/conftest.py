import asyncio
import json
from dataclasses import dataclass
from typing import Optional
from uuid import uuid4


import aiohttp
import aioredis
import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from functional.config import DatabaseConfig, TestFilesPath
from functional.settings import TestSettings
from functional.models import Base, User, Role, RolesUsers, LoginHistory, AuthToken
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


@pytest.fixture(scope="session")
async def cache_client():
    client = await aioredis.create_redis_pool((settings.redis_host, settings.redis_port), minsize=10, maxsize=20)
    yield aioredis.Redis(client)
    await client.flushdb()
    client.close()


@pytest.fixture(scope="session")
def db_conn():
    return db_config.ENGINE.connect()


@pytest.fixture(scope="session")
def setup_database(db_conn):
    meta = Base.metadata
    meta.bind = db_conn
    meta.create_all()
    yield

@pytest.fixture
def db_session(setup_database, db_conn):
    transaction = db_conn.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=db_conn)
    )
    transaction.rollback()


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
    async def inner(url: str, data: dict, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        async with session.post(url, json=data) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture()
async def roles_to_pg(db_session):
    roles = [
        {
            "id": "6d12302c-6e39-4b83-aa94-c21de1a76e0e",
            "name": "user",
            "description": "description",
        },
        {
            "id": "6d12302c-6e39-4b83-aa94-c21de1a76e0a",
            "name": "admin",
            "description": "description",
        }
    ]

    for role in roles:
        db_role = Role(**role)
        db_session.add(db_role)
    db_session.commit()
