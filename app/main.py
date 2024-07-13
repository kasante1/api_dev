from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from . import schemas
from typing import List


from . import models, utils
from .database import engine, get_db
from sqlalchemy.orm import Session

from .routers import users, posts

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(posts.router)
app.include_router(users.router)