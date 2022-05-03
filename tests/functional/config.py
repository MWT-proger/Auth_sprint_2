import os

from sqlalchemy import MetaData, create_engine
from functional.settings import TestSettings

settings = TestSettings()
BASE_URL_V1 = "{protocol}://{host}:{port}/auth/api/v1".format(protocol=settings.service_protocol,
                                                              host=settings.service_host,
                                                              port=settings.service_port)
BASE_TEST_PATH = "tests/functional/testdata/"


class TestUrls:
    registration: str = BASE_URL_V1 + "/users/registration"


class TestFilesPath:
    registration: str = BASE_TEST_PATH + "registration.json"


class DatabaseConfig:
    ENGINE = create_engine("postgresql://{user}:{password}@{host}:{port}/{database_name}".format(
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database_name=settings.db_database_name,
    ))
    TRACK_MODIFICATIONS = False
    SCHEMA = settings.db_scheme
    metadata = MetaData(schema=settings.db_scheme)
