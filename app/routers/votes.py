from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas

from .. import models, utils, oauth
from ..database import get_db  
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED,
            )
def vote(vote: schemas.Votes, db: Session = Depends(get_db),
         current_user = Depends(oauth.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {vote.post_id} not found"
        )

    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id
    )
    
    found_vote = vote_query.first()

    if vote.vote == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}"
            )
        new_vote = models.Votes(post_id = vote.post_id, user_id=current_user.id)

        db.add(new_vote)
        db.commit()
        return {"message": "vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="nonexistent vote"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return  {"message": "vote deleted"}
