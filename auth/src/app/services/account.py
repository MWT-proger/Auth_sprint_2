from datetime import datetime

from config import get_config as config
from database import db
from models import LoginHistory
from redis import Redis
from redis_db import redis_conn
from services.auth_token import get_auth_token_service as auth_token_service
from services.user import get_user_service as user_service
from werkzeug.security import check_password_hash


class AccountService:

    def __init__(self):
        self.storage: Redis = redis_conn
        self.db_session = db.session

    def add_login_history(self, user_id: str, user_agent: str):
        login_history = LoginHistory(user_id=user_id, user_agent=user_agent)
        self.db_session.add(login_history)
        return login_history

    def login(self, login: str, password: str, user_agent: str):
        user = user_service.get_by_login(login)
        if not user or not check_password_hash(user._password, password):
            return

        self.add_login_history(user_id=user.id, user_agent=user_agent.string)
        access, refresh = auth_token_service.get_tokens_pair(user.id)
        auth_token_service.add_or_update_refresh_token(user_id=user.id, refresh_token=refresh, user_agent=user_agent)

        self.db_session.commit()
        return access, refresh

    def logout(self, user_id: str, jti: str, user_agent: str):
        key = "revoked_token_%s" % jti

        self.storage.set(key, "", ex=config.JWT.ACCESS_EXPIRE)
        auth_token_service.delete_refresh_token(user_id=user_id, user_agent=user_agent)

        self.db_session.commit()

    def full_logout(self, user_id: str):
        key = "full_logout_%s" % user_id

        self.storage.set(key, datetime.now().timestamp(), ex=config.JWT.ACCESS_EXPIRE)
        auth_token_service.delete_all_refresh_token(user_id=user_id)

        self.db_session.commit()


get_account_service = AccountService()
