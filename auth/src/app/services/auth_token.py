from database import db
from models import User, LoginHistory, AuthToken


class AuthTokenService:

    def __init__(self):
        self.model = AuthToken
        self.db_session = db.session

    def add_or_update_refresh_token(self, user_id: str, refresh_token: str, user_agent: str):
        token = self.get_refresh_token(user_id=user_id, user_agent=user_agent)
        if token:
            token.refresh_token = refresh_token
        else:
            token = self.model(user_id=user_id, refresh_token=refresh_token, user_agent=user_agent.string)
            self.db_session.add(token)
        return token

    def get_refresh_token(self, user_id: str, user_agent: str = None, all: bool = None):
        if all:
            query = self.model.query.filter_by(user_id=user_id)
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
