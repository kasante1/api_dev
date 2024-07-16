from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import config

app_env = config.application_env

DATABASE_URL = f"{app_env.DATABASE_TYPE}://{app_env.DATABASE_USER_NAME}:{app_env.DATABASE_PASSWORD}@{app_env.DATABASE_HOST}/{app_env.DATABASE_NAME}"

engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
Base = declarative_base() 
