import os
from datetime import timedelta


class AppConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")


class DatabaseConfig:
    URI = "postgresql://{user}:{password}@{host}:{port}/{database_name}" \
        .format(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT")),
                database_name=os.getenv("DB_NAME"),
                )
    TRACK_MODIFICATIONS = False
    SCHEMA = "content"


class SecurityConfig:
    SALT = "salt"
    HASH = "sha512_crypt"


class JWTConfig:
    SECRET_KEY = "super-secret"
    ACCESS_EXPIRE = timedelta(minutes=5)
    REFRESH_EXPIRE = timedelta(days=15)


class RedisConfig:
    HOST = os.getenv("REDIS_HOST")
    PORT = os.getenv("REDIS_PORT")


class Config:
    JWT: JWTConfig = JWTConfig()
    DB: DatabaseConfig = DatabaseConfig()
    security: SecurityConfig = SecurityConfig()
    REDIS: RedisConfig = RedisConfig()
    APP: AppConfig = AppConfig()


get_config = Config()
