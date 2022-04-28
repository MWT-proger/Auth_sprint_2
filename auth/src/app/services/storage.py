from redis_db import redis_conn
from redis import Redis


class TokenStorageError(Exception):
    pass


class TokenStorage:
    def __init__(self):
        self.storage: Redis = redis_conn

    def add_invalid_access(self,  token, user_id, expire):
        self._execute(self.storage.set, name=token, value=str(user_id), ex=expire)

    def is_valid_access(self, token):
        return not bool(self._execute(self.storage.exists, token))

    @staticmethod
    def _execute(method, *args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as err:
            print(err)
            raise TokenStorageError


token_storage = TokenStorage()
