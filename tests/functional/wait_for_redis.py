from redis import Redis
from settings import TestSettings
from utils.app_logger import get_logger
from utils.backoff import backoff

settings = TestSettings()
logger = get_logger('Redis connection')


@backoff()
def wait_for_redis():
    logger.info("start")
    redis = Redis(settings.redis_host)
    redis.ping()
    logger.info("successful connection!")


if __name__ == "__main__":
    wait_for_redis()
