from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    db_host: str = Field("host.docker.internal", env="DB_HOST")
    db_port: str = Field("9200", env="DB_PORT")

    redis_host: str = Field("host.docker.internal", env="REDIS_HOST")
    redis_port: str = Field("6379", env="REDIS_PORT")

    service_protocol: str = Field("http", env="SERVICE_PROTOCOL")
    service_host: str = Field("host.docker.internal", env="SERVICE_HOST")
    service_port: str = Field("5000", env="SERVICE_PORT")


