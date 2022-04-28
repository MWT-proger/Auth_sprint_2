from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from werkzeug.security import check_password_hash, generate_password_hash
from redis_db import redis_conn
from redis import Redis

from config import Config
from database import db
from models import User, LoginHistory, AuthToken
from services.user import get_user_service as user_service
from services.auth_token import get_auth_token_service as auth_token_service

config = Config()

class AccountService:

    def __init__(self):
        self.storage: Redis = redis_conn
        self.db_session = db.session

    @staticmethod
    def get_tokens_pair(user_id: str):
        access = create_access_token(identity=user_id)
        refresh = create_refresh_token(identity=user_id)

        return access, refresh

    def refresh_token_pair(self, user_id):

        # TODO ДОБАВИТЬ УДАЛЕНИЕ СТАРОГО REFRESH ТОКЕНА

        return self.get_tokens_pair(user_id)

    def add_login_history(self, user_id: str, user_agent: str):
        login_history = LoginHistory(user_id=user_id, user_agent=user_agent)
        self.db_session.add(login_history)
        return login_history

    def login(self, login: str, password: str, user_agent: str):
        user = user_service.get_by_login(login)
        if not user or not check_password_hash(user._password, password):
            return

        self.add_login_history(user_id=user.id, user_agent=user_agent.string)
        access, refresh = self.get_tokens_pair(user.id)
        auth_token_service.add_or_update_refresh_token(user_id=user.id, refresh_token=refresh, user_agent=user_agent)

        self.db_session.commit()
        return access, refresh

    def logout(self, user_id: str, jti: str, user_agent: str):
        self.storage.set(jti, "", ex=config.JWT.ACCESS_EXPIRE)
        auth_token_service.delete_refresh_token(user_id=user_id, user_agent=user_agent)
        self.db_session.commit()

get_account_service = AccountService()
