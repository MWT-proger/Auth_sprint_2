import asyncio
from dataclasses import dataclass
from typing import Optional

import aiohttp
import aioredis
import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from functional.config import DatabaseConfig, TestFilesPath, TestUrls
from functional.settings import TestSettings
from functional.utils import get_data
from functional.testdata import data_account
from functional.testdata import role_data
from functional.models import Base, User, Role, RolesUsers, LoginHistory, AuthToken
from multidict import CIMultiDictProxy

settings = TestSettings()
db_config = DatabaseConfig()
test_data = TestFilesPath()
urls = TestUrls()


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
    meta.drop_all()


@pytest.fixture
def db_session(setup_database, db_conn):
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=db_conn)
    )


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        async with session.get(url, params=params, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_post_request(session):
    async def inner(url: str, data: dict = None, headers: Optional[dict] = None) -> HTTPResponse:
        async with session.post(url, json=data, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_put_request(session):
    async def inner(url: str, data: dict = None, headers: Optional[dict] = None) -> HTTPResponse:
        async with session.put(url, json=data, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_delete_request(session):
    async def inner(url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> HTTPResponse:
        async with session.delete(url, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


class DBManager:
    def __init__(self, model: Base, db_session, data=None, path_file: str = None):
        self.db_session = db_session
        self.path_file = path_file
        self.data = data
        self.model = model

    async def add_dada(self):
        if not self.data:
            self.data = await get_data.from_file(self.path_file)

        if isinstance(self.data, list):
            for obj in self.data:
                db_obj = self.model(**obj)
                self.db_session.add(db_obj)
        else:
            db_obj = self.model(**self.data)
            self.db_session.add(db_obj)
        self.db_session.commit()

    async def delete_dada(self):
        self.db_session.query(self.model).delete()
        self.db_session.commit()


@pytest.fixture
async def role_reg_to_pg(db_session):
    manager_db = DBManager(db_session=db_session, data=data_account.roles, model=Role)
    await manager_db.add_dada()
    yield
    db_session.query(RolesUsers).delete()
    db_session.query(User).delete()
    await manager_db.delete_dada()


@pytest.fixture
async def account_user_to_pg(db_session):
    manager_db = DBManager(db_session=db_session, data=data_account.users, model=User)
    await manager_db.add_dada()
    yield
    db_session.query(RolesUsers).delete()
    await manager_db.delete_dada()


@pytest.fixture
async def delete_data_all(db_session):
    yield True
    db_session.query(RolesUsers).delete()
    db_session.query(LoginHistory).delete()
    db_session.query(AuthToken).delete()
    db_session.query(User).delete()
    db_session.query(Role).delete()

    db_session.commit()


@pytest.fixture
async def data_to_pg(db_session):
    try:
        db_user = User(**role_data.user)
        db_session.add(db_user)
        db_session.commit()

        for role in role_data.roles:
            db_role = Role(**role)
            db_session.add(db_role)
        db_session.commit()

        db_user_role = RolesUsers(**role_data.user_role)
        db_session.add(db_user_role)
        db_session.commit()
    except Exception as e:
        db_session.rollback()


@pytest.fixture
async def get_access(make_post_request):
    response = await make_post_request(urls.login, data={
        "login": "USER",
        "_password": "12345"
    })

    return response.body["access_token"]
