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

    login: str = AUTH_URL_V1 + "/login"
    protected: str = AUTH_URL_V1 + "/protected"
    refresh: str = AUTH_URL_V1 + "/refresh"
    logout: str = AUTH_URL_V1 + "/logout"
    full_logout: str = AUTH_URL_V1 + "/full_logout"

    registration: str = AUTH_URL_V1 + "/users/registration"
    users_my: str = AUTH_URL_V1 + "/users/my"
    my_login_history: str = AUTH_URL_V1 + "/users/my_login_history"

    get_all_roles: str = ROLE_URL_V1
    get_user_role: str = AUTH_URL_V1 + "/users/roles"
    add_new_role: str = ROLE_URL_V1 + "/create"
    delete_role: str = ROLE_URL_V1
    add_role_to_user = AUTH_URL_V1 + "/users/roles"


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
