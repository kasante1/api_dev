from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)



app = FastAPI()


class PostValidator(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/sqlalchemy")
def test_endpoints(db: Session = Depends(get_db)):
    return {"status": "success"}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: PostValidator, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}

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
