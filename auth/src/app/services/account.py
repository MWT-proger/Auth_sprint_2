from models import User
from flask_jwt_extended import create_access_token, create_refresh_token


class AccountService:

    def get_tokens_pair(self, user: User):
        access = create_access_token(identity=user.id)
        refresh = create_refresh_token(identity=user.id)

        return access, refresh
