
from fastapi import FastAPI, Query, Response, status, HTTPException, Depends , APIRouter
from typing import  List, Optional
from sqlalchemy.orm import Session
from database import engine , get_db
import models, schemas, utils
import oauth2

router=APIRouter(
    prefix="/vote",
        tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db: Session = Depends(get_db), current_user: schemas.UserModel = Depends(oauth2.get_current_user)):
    post= db.query(models.Post).filter(models.Post.id==vote.post_id).first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {vote.post_id} does not exist")

    vote_query=db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()

    if(vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=f"Unauthorized used") 
        new_vote=models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Vote successful"}

    else: 
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=f"Unauthorized used") 
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Vote deleted successfully"}


    

    # if(search==""):
    #     post= db.query(models.Post).all()
    # else:
    #     post= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
    # # post= db.query(models.Post).all()
    # # post= db.query(models.Post).filter(models.Post.user_id==current_user.id).all()


    return post