from models import User
from flask_jwt_extended import create_access_token, create_refresh_token


class AccountService:

    @staticmethod
    def get_tokens_pair(user_id: str):
        access = create_access_token(identity=user_id)
        refresh = create_refresh_token(identity=user_id)

        return access, refresh

    def refresh_token_pair(self, user_id):

        # TODO ДОБАВИТЬ УДАЛЕНИЕ СТАРОГО REFRESH ТОКЕНА

        return self.get_tokens_pair(user_id)

    def add_login_entry(self):
        pass
