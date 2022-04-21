from settings import Settings

settings = Settings()


class DatabaseConfig:
    DATABASE_URI = "postgresql://<{user}>:<{password}>@<{host}>/<{database_name}>".format(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        database_name=settings.POSTGRES_NAME
    )
    TRACK_MODIFICATIONS = False
    SCHEMA = "content"


class Config:
    DB: DatabaseConfig = DatabaseConfig()
