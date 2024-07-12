from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from . import config
import time
from functools import lru_cache


app = FastAPI()

class PostValidator(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@lru_cache
def get_db_settings():
    return config.DBConnDetails(_env_file='.env', _env_file_encoding='utf-8')

conn_details = get_db_settings()

# while True:
try:
    conn = psycopg2.connect(
        host=conn_details.host,
        database=conn_details.database,
        user=conn_details.databaseuser,
        password=conn_details.password,
        cursor_factory=RealDictCursor
    )

    cursor = conn.cursor()
    print("Database connection was successful!")
        # break
except KeyboardInterrupt:
    print("Connection terminated manually !!!")
except Exception as error:
    print("Connecting to the database failed!")
    print("Error: ", error)
        # time.sleep(3)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(payLoad: PostValidator):
    return {"data": payLoad}

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    # response.status_code = status.HTTP_404_NOT_FOUND
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found"
    )

    
    return {"post details": f"{id}"}

@app.get("/posts/latest")
async def get_latest_post():
    return {}
