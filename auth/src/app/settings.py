from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    POSTGRES_USER: str = Field(env="DB_USER")
    POSTGRES_PASSWORD: str = Field(env="DB_PASSWORD")
    POSTGRES_NAME: str = Field(env="DB_NAME")
    POSTGRES_HOST: str = Field(env="DB_HOST")
    POSTGRES_PORT: str = Field(env="DB_PORT")
