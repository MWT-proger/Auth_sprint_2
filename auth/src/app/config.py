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
    ACCESS_EXPIRE = timedelta(minutes=15)
    REFRESH_EXPIRE = timedelta(days=15)


class RedisConfig:
    HOST = os.getenv("REDIS_HOST")
    PORT = os.getenv("REDIS_PORT")


class RateLimit:
    MAX_CALLS = 1000
    TIME = 59


class Jaeger:
    PORT = os.getenv("JAEGER_PORT")
    HOST = os.getenv("JAEGER_HOST")


class Oauth:
    YANDEX_ID = os.getenv("OAUTH_YANDEX_ID")
    YANDEX_SECRET = os.getenv("OAUTH_YANDEX_SECRET")
    MAIL_ID = os.getenv("OAUTH_MAIL_ID")
    MAIL_SECRET = os.getenv("OAUTH_MAIL_SECRET")
    VK_ID = os.getenv("OAUTH_VK_ID")
    VK_SECRET = os.getenv("OAUTH_VK_SECRET")


class ReCaptcha:
    RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")


class Config:
    JWT: JWTConfig = JWTConfig()
    DB: DatabaseConfig = DatabaseConfig()
    security: SecurityConfig = SecurityConfig()
    REDIS: RedisConfig = RedisConfig()
    APP: AppConfig = AppConfig()
    RATE_LIMIT: RateLimit = RateLimit()
    JAEGER: Jaeger = Jaeger()
    OAUTH: Oauth = Oauth()
    RECAPTCHA: ReCaptcha = ReCaptcha()


get_config = Config()
