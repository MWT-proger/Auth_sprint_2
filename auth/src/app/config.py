from flask_marshmallow import Marshmallow
from settings import Settings

settings = Settings()


class DatabaseConfig:
    URI = "postgresql://{user}:{password}@{host}:{port}/{database_name}".format(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database_name=settings.POSTGRES_NAME
    )
    TRACK_MODIFICATIONS = False
    SCHEMA = "content"


class SecurityConfig:
    SALT = "salt"
    HASH = "sha512_crypt"


class JWTSettings:
    SECRET_KEY = "super-secret"


class Config:
    JWT: JWTSettings = JWTSettings()
    DB: DatabaseConfig = DatabaseConfig()
    security: SecurityConfig = SecurityConfig()
