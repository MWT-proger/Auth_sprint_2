from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    db_user = Field("admin", env="DB_USER")
    db_password = Field("password", env="DB_PASSWORD")
    db_host = Field("host.docker.internal", env="DB_HOST")
    db_port = Field(5433, env="DB_PORT")
    db_database_name = Field("auth_database", env="DB_NAME")
    db_scheme = "content"

    redis_host: str = Field("host.docker.internal", env="REDIS_HOST")
    redis_port: str = Field("6379", env="REDIS_PORT")

    service_protocol: str = Field("http", env="SERVICE_PROTOCOL")
    service_host: str = Field("localhost", env="SERVICE_HOST")
    service_port: str = Field("80", env="SERVICE_PORT")


