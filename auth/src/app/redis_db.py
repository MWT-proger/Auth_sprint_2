from config import get_config as config
from redis import StrictRedis

redis_conn = StrictRedis(
    host=config.REDIS.HOST, port=config.REDIS.PORT, decode_responses=True
)
