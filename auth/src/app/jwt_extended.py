from config import Config
from flask import Flask
from flask_jwt_extended import JWTManager

jwt = JWTManager()
config = Config()


def init_jwt(app: Flask):
    app.config["JWT_SECRET_KEY"] = config.JWT.SECRET_KEY

    jwt.init_app(app)
