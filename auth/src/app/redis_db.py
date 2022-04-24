from redis import StrictRedis
from config import Config

config = Config()

redis_conn = StrictRedis(
    host=config.REDIS.HOST, port=config.REDIS.PORT, decode_responses=True
)
