import os
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class ApplicationEnv(BaseSettings):

    DEBUG: Optional[bool] = os.getenv("DEBUG") == "True"
    POSTGRES_DATABASE_URL: str = os.getenv("DATABASE_URL")

    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
    ALGORITHM: Optional[str] = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

application_env = ApplicationEnv()
