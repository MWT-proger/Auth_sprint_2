from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

from models import User
from database import db


class UserService:
    model = User

    def __init__(self):
        return

    def create(self, login: str, email: str, password: str):
        hashed_password = generate_password_hash(password)
        new_user = self.model(login=login, _password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_by_login(self, login: str):
        user = self.model.query.filter_by(login=login).first()
        return user

    def get_by_email(self, email: str):
        user = self.model.query.filter_by(email=email).first()
        return user

    def login(self, login: str, password: str):
        user = self.get_by_login(login)
        if not user or not check_password_hash(user._password, password):
            return
        return user



