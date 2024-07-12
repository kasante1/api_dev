from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConnDetails(BaseSettings):
    host: str
    database: str
    databaseuser: str
    password: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


# class DBConnDetails(BaseSettings):
#     host: str = "localhost"
#     database: str = "posts"
#     databaseuser: str = "postgres"
#     password: str = "postgres"

