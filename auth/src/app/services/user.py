from api.v1.response_code import get_error_response as error_response
from database import db
from datastore import datastore
from models import LoginHistory, RoleEnum, User
from werkzeug.security import generate_password_hash
from http import HTTPStatus


class UserService:
    model = User
    db_session = db.session

    def __init__(self):
        return

    def check_exist_email(self, email):
        is_existed_email = self.get_by_email(email)
        if is_existed_email:
            return error_response.fail({"email": "email already exists"}, status_code=HTTPStatus.BAD_REQUEST)

    def check_exist_login(self, login):
        is_existed_login = self.get_by_login(login)
        if is_existed_login:
            return error_response.fail({"login": "login already exists"}, status_code=HTTPStatus.BAD_REQUEST)

    def create(self, data: dict):
        login = data.get("login")
        password = data.get("_password")
        email = data.get("email")

        self.check_exist_email(email)
        self.check_exist_login(login)

        hashed_password = generate_password_hash(password)
        new_user = datastore.create_user(login=login, email=email, _password=hashed_password)

        datastore.add_role_to_user(new_user, RoleEnum.user.value)
        db.session.commit()

        return new_user, False

    def update(self, user_id: str, data: dict):
        login = data.get("login")
        password = data.get("_password")
        email = data.get("email")
        update_status = False

        user = self.get_by_user_id(user_id)

        if login and login != user.login:
            self.check_exist_login(login)

            user.login = login
            update_status = True

        if email and email != user.email:
            self.check_exist_email(email)

            user.email = email
            update_status = True

        if password:
            hashed_password = generate_password_hash(password)
            user._password = hashed_password
            update_status = True

        if update_status:
            self.db_session.add(user)
            self.db_session.commit()

        return user, False

    def get_by_login(self, login: str):
        user = self.model.query.filter_by(login=login).first()
        return user

    def get_by_email(self, email: str):
        user = self.model.query.filter_by(email=email).first()
        return user

    def get_by_user_id(self, user_id: str):
        user = self.model.query.filter_by(id=user_id).first()
        return user

    def get_login_history(self, user_id: str):
        query = LoginHistory.query.filter_by(user_id=user_id).all()
        return query, False


get_user_service = UserService()
