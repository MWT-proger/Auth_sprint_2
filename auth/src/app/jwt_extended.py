from config import get_config as config
from flask import Flask
from flask_jwt_extended import JWTManager

jwt = JWTManager()


def init_jwt(app: Flask):
    app.config["JWT_SECRET_KEY"] = config.JWT.SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT.ACCESS_EXPIRE
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = config.JWT.REFRESH_EXPIRE

    jwt.init_app(app)
