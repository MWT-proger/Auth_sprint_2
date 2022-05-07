import os

from settings import TestSettings
from sqlalchemy import create_engine
from utils.app_logger import get_logger
from utils.backoff import backoff

settings = TestSettings()
logger = get_logger('DB connection')


@backoff()
def wait_for_db():
    logger.info("start")

    engine = create_engine("postgresql://{user}:{password}@{host}:{port}/{database_name}".format(
                user=settings.db_user,
                password=settings.db_password,
                host=settings.db_host,
                port=settings.db_port,
                database_name=settings.db_database_name,
                ))

    engine.connect()
    logger.info("successful connection!")


if __name__ == "__main__":
    wait_for_db()
