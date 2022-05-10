from http import HTTPStatus

from datetime import datetime
import pyotp
from config import get_config as config
from database import db
from models import LoginHistory, MultiFactorAuthentication
from redis import Redis
from redis_db import redis_conn
from api.v1.response_code import get_error_response as error_response
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

    def get_mf_auth(self, user_id: str):
        mf_auth = MultiFactorAuthentication.query.filter_by(user_id=user_id).first()
        return mf_auth

    def add_or_update_mf_auth(self, user_id: str):
        secret = pyotp.random_base32()
        mf_auth = self.get_mf_auth(user_id=user_id)
        if not mf_auth:
            mf_auth = MultiFactorAuthentication(user_id=user_id, secret=secret)
            self.db_session.add(mf_auth)
        else:
            mf_auth.status = False
            mf_auth.secret = secret
        self.db_session.commit()
        return mf_auth

    def update_mf_auth(self, mf_auth: MultiFactorAuthentication, status: bool):
        mf_auth.status = status
        self.db_session.commit()
        return mf_auth

    def login(self,
              user_agent: str,
              user=None,
              login: str = None,
              password: str = None,
              code_2fa: str = None,
              without_verification: bool = False):
        if not without_verification or not user:
            user = user_service.get_by_login(login)
            if not user or not check_password_hash(user._password, password):
                return None
            mf_auth = MultiFactorAuthentication.query.filter_by(user=user, status=True).first()

            if mf_auth:
                totp = pyotp.TOTP(mf_auth.secret)
                if not totp.verify(code_2fa):
                    return error_response.fail({"code_2fa": "Enter a valid 2FA code"}, status_code=HTTPStatus.BAD_REQUEST)

        access, refresh = auth_token_service.get_tokens_pair(user.id)

        self.add_login_history(user_id=user.id, user_agent=user_agent.string)
        auth_token_service.add_or_update_refresh_token(user_id=user.id, refresh_token=refresh, user_agent=user_agent)

        self.db_session.commit()
        return access, refresh

    def logout(self, user_id: str, jti: str, user_agent: str):
        key = f"revoked_token_{jti}"

        self.storage.set(key, "1", ex=config.JWT.ACCESS_EXPIRE)
        auth_token_service.delete_refresh_token(user_id=user_id, user_agent=user_agent)

        self.db_session.commit()

    def full_logout(self, user_id: str):
        key = f"full_logout_{user_id}"

        self.storage.set(key, datetime.now().timestamp(), ex=config.JWT.ACCESS_EXPIRE)
        auth_token_service.delete_all_refresh_token(user_id=user_id)

        self.db_session.commit()


get_account_service = AccountService()
