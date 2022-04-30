from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore

from database import db
from models import Role, User

datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()


def init_datastore(app: Flask):
    security.init_app(app, datastore)
