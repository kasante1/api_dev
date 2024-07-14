from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas
from typing import List, Optional


from .. import models, utils, oauth
from ..database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/public-posts", response_model=List[(schemas.PublicPost)])
def get_all_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "" ):

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no post(s) found"
        )
    return  posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth.get_current_user)
    ):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post

@router.get("/user-post", response_model=List[(schemas.Post)])
def get_user_post(db: Session = Depends(get_db),
                current_user: int = Depends(oauth.get_current_user)):

    post = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id
    ).all()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no post(s) found"
        )

    return post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth.get_current_user)):

    post = db.query(models.Post).filter(
        models.Post.id == id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Not Authorized"
        )


    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth.get_current_user)
                ):

    post_query = db.query(models.Post).filter(
        models.Post.id == id
    )

    post = post_query.first()
    
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Not Authorized"
        )

    
    post_query.delete(synchronize_session=False)
    db.commit()

    return  delete_post

@router.put("/{id}")
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db),
                current_user = Depends(oauth.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    db_post = post_query.first()

    if db_post == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exit"
        )
    
    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Not Authorized"
        )

    post_query.update(post.model_dump(), synchronize_session=False)
    
    db.commit()

    return  post_query.first()

 
