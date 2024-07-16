import os
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class ApplicationEnv(BaseSettings):
    DEBUG: Optional[bool] = os.getenv("DEBUG") == "True"
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
    ALGORITHM: Optional[str] = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    DATABASE_TYPE: str = os.getenv("DATABASE_HOSTNAME")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT")
    DATABASE_USER_NAME: str = os.getenv("DATABASE_USER_NAME")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST")


application_env = ApplicationEnv()
