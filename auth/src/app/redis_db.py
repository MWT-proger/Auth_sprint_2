from redis import StrictRedis

from config import get_config as config

redis_conn = StrictRedis(
    host=config.REDIS.HOST, port=config.REDIS.PORT, decode_responses=True
)
