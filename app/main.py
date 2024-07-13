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

@app.get("/sqlalchemy")
def test_endpoints(db: Session = Depends(get_db)):
    return {"status": "success"}

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: PostValidator, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):

    # response.status_code = status.HTTP_404_NOT_FOUND
    post = db.query(models.Post).filter(
        models.Post.id == id
    ).all()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    delete_post_query = db.query(models.Post).filter(
        models.Post.id == id
    )

    if delete_post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )
    
    delete_post_query.delete(synchronize_session=False)
    db.commit()

    
    return {"data": delete_post}

@app.put("/posts/{id}")
def update_post(id: int, post: PostValidator, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    db_post = post_query.first()

    if db_post == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exit"
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    
    db.commit()

    return {"data": post_query.first()}
@app.get("/posts/latest")
def get_latest_post():
    return {}
