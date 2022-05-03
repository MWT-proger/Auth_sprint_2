import os

from sqlalchemy import create_engine
from functional.settings import TestSettings

settings = TestSettings()
BASE_AUTH_URL_V1 = "{protocol}://{host}:{port}/auth/api/v1".format(protocol=settings.service_protocol,
                                                                   host=settings.service_host,
                                                                   port=settings.service_port)
BASE_ROLE_URL_V1 = "{protocol}://{host}:{port}/role/api/v1".format(protocol=settings.service_protocol,
                                                                   host=settings.service_host,
                                                                   port=settings.service_port)
BASE_TEST_PATH = "tests/functional/testdata/"


class TestUrls:
    registration: str = BASE_AUTH_URL_V1 + "/users/registration"
    get_all_roles: str = BASE_ROLE_URL_V1


class TestFilesPath:
    registration: str = BASE_TEST_PATH + "registration.json"


class DatabaseConfig:
    ENGINE = create_engine("postgresql://{user}:{password}@{host}:{port}/{database_name}".format(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 5433)),
        database_name=os.getenv("DB_NAME"),
    ))
    TRACK_MODIFICATIONS = False
    SCHEMA = "content"
