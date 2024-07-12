from pydantic_settings import BaseSettings, SettingsConfigDict
class DBConnUrl(BaseSettings):
    databaseurl: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
