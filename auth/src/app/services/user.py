from http import HTTPStatus

from api.v1.response_code import get_error_response as error_response
from database import db, session_scope
from datastore import datastore
from models import LoginHistory, RoleEnum, User, SocialAccount
from werkzeug.security import generate_password_hash, check_password_hash
from utils import generate


class UserService:
    model = User
    db_session = db.session

    def __init__(self):
        return

    def check_exist_email(self, email):
        is_existed_email = self.get_by_email(email)
        if is_existed_email:
            return error_response.fail({"email": "email already exists"}, status_code=HTTPStatus.BAD_REQUEST)

    def check_old_password(self, user, old_password):
        if not check_password_hash(user._password, old_password):
            return error_response.fail({"old_password": "Old password is incorrect"},
                                       status_code=HTTPStatus.BAD_REQUEST)

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

    def create_oauth(self, login: str, email: str, social_id: str, social_name: str):
        is_existed_email = self.get_by_email(email)
        if is_existed_email:
            while self.get_by_email(email):
                name = generate.random_name(8)
                email = f"{name}@mail.ru"

        is_existed_login = self.get_by_login(login)
        if is_existed_login:
            while self.get_by_login(login):
                login = generate.random_name(8)

        password = generate.random_string()
        # TODO Потом будем отправлять на почту пользователю
        hashed_password = generate_password_hash(password)
        with session_scope() as session:
            new_user = datastore.create_user(login=login, email=email, _password=hashed_password)
            social_account = SocialAccount(user=new_user, social_id=social_id, social_name=social_name)
            session.add(social_account)
            datastore.add_role_to_user(new_user, RoleEnum.user.value)

        return new_user

    def change_password(self, user_id: str, data: dict):
        password = data.get("_password")
        old_password = data.get("old_password")

        user = self.get_by_user_id(user_id)

        self.check_old_password(user, old_password)

        hashed_password = generate_password_hash(password)
        user._password = hashed_password

        self.db_session.add(user)
        self.db_session.commit()
        return True

    def update(self, user_id: str, data: dict):
        login = data.get("login")
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
