from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from . import schemas
from typing import List

from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    # response.status_code = status.HTTP_404_NOT_FOUND
    post = db.query(models.Post).filter(
        models.Post.id == id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    return post


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

    
    return  delete_post

@app.put("/posts/{id}")
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    db_post = post_query.first()

    if db_post == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exit"
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    
    db.commit()

    return  post_query.first()
@app.get("/posts/latest")
def get_latest_post():
    return {}
