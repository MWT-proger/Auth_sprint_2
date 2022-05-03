import os

from sqlalchemy import create_engine
from settings import TestSettings
from utils.app_logger import get_logger
from utils.backoff import backoff

settings = TestSettings()
logger = get_logger('DB connection')


@backoff()
def wait_for_db():
    logger.info("start")

    engine = create_engine("postgresql://{user}:{password}@{host}:{port}/{database_name}".format(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT")),
                database_name=os.getenv("DB_NAME"),
                ))

    db = engine.connect()
    logger.info(db)
    logger.info("successful connection!")


if __name__ == "__main__":
    wait_for_db()
