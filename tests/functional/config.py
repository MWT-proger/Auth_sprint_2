from sqlalchemy import MetaData, create_engine
from functional.settings import TestSettings

settings = TestSettings()

BASE = "{protocol}://{host}:{port}".format(protocol=settings.service_protocol,
                                           host=settings.service_host,
                                           port=settings.service_port)

AUTH_URL_V1 = f"{BASE}/auth/api/v1"
ROLE_URL_V1 = f"{BASE}/role/api/v1"

BASE_TEST_PATH = "tests/functional/testdata/"


class TestUrls:
    registration: str = AUTH_URL_V1 + "/users/registration"
    login: str = AUTH_URL_V1 + "/login"
    get_all_roles: str = ROLE_URL_V1
    get_user_role: str = AUTH_URL_V1 + "/users/roles"
    add_new_role: str = ROLE_URL_V1 + "/create"
    delete_role: str = ROLE_URL_V1


class TestFilesPath:
    registration: str = BASE_TEST_PATH + "registration.json"
    roles_for_registration: str = BASE_TEST_PATH + "roles_for_registration.json"
    account_user: str = BASE_TEST_PATH + "account_user.json"


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
