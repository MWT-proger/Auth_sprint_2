from database import db
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt
from models import AuthToken


class AuthTokenService:

    def __init__(self):
        self.model = AuthToken
        self.db_session = db.session

    @staticmethod
    def get_tokens_pair(user_id: str):

        access = create_access_token(identity=user_id)
        refresh = create_refresh_token(identity=user_id)

        return access, refresh

    def add_or_update_refresh_token(self, user_id: str, refresh_token: str, user_agent: str):
        token = self.get_refresh_token(user_id=user_id, user_agent=user_agent)
        if token:
            token.refresh_token = refresh_token
        else:
            token = self.model(user_id=user_id, refresh_token=refresh_token, user_agent=user_agent.string)
            self.db_session.add(token)
        return token

    def update_refresh_token(self, user_id: str, refresh_token: str):
        token = self.get_refresh_token(user_id=user_id, refresh=refresh_token)
        if not token:
            return None, None
        access_token, new_refresh = self.get_tokens_pair(user_id=user_id)
        token.refresh_token = new_refresh
        self.db_session.add(token)
        self.db_session.commit()
        return access_token, new_refresh

    def get_refresh_token(self, user_id: str, user_agent: str = None, all: bool = None, refresh: str = None):
        if all:
            query = self.model.query.filter_by(user_id=user_id)
        elif refresh:
            query = self.model.query.filter_by(user_id=user_id, refresh_token=refresh).first()
        else:
            query = self.model.query.filter_by(user_id=user_id, user_agent=user_agent.string).first()
        return query

    def delete_refresh_token(self, user_id: str, user_agent: str):
        token = self.get_refresh_token(user_id=user_id, user_agent=user_agent)
        if token:
            self.db_session.delete(token)

    def delete_all_refresh_token(self, user_id: str):
        tokens = self.get_refresh_token(user_id=user_id, all=True)
        if tokens:
            for token in tokens:
                self.db_session.delete(token)


get_auth_token_service = AuthTokenService()
