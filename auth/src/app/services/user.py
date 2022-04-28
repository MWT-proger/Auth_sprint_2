from database import db
from datastore import datastore
from models import RoleEnum, User
from werkzeug.security import check_password_hash, generate_password_hash


class UserService:
    model = User

    def __init__(self):
        return

    def create(self, login: str, email: str, password: str):
        hashed_password = generate_password_hash(password)
        new_user = datastore.create_user(login=login, email=email, _password=hashed_password)
        datastore.add_role_to_user(new_user, RoleEnum.user.value)
        db.session.commit()
        return new_user

    def get_by_login(self, login: str):
        user = self.model.query.filter_by(login=login).first()
        return user

    def get_by_email(self, email: str):
        user = self.model.query.filter_by(email=email).first()
        return user


get_user_service = UserService()
