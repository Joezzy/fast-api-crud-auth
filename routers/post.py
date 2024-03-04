
from typing import  List, Optional
from sqlalchemy.orm import Session
from database import engine , get_db
from fastapi import FastAPI, Query, Response, status, HTTPException, Depends , APIRouter
from  fastapi.responses import ORJSONResponse
import models, schemas, utils
import oauth2
from sqlalchemy import func

router=APIRouter(
    prefix="/post",
        tags=["Post endpoint"]
)


@router.get("/", response_model=List[schemas.PostVoteResponse])
# @router.get("/")
def get_posts(search:Optional[str]="",limit:int=50, offset:int=0, db: Session = Depends(get_db), current_user: schemas.UserModel = Depends(oauth2.get_current_user)):
    

    # if(search==""):
    #     post= db.query(models.Post).all()
    # else:
    # post= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

    # post= db.query(models.Post).all()
    # post= db.query(models.Post).filter(models.Post.user_id==current_user.id).all()


    if(search==""):
        result=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id==models.Post.id, isouter=True
             ).group_by(models.Post.id).all()
    else:
        result=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True
        ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
        print(result)

    return result
 
    # return {"data": post}

@router.get("/{id}",status_code=status.HTTP_200_OK, response_model=schemas.PostVoteResponse)
def get_post_by_id(id:int, db: Session = Depends(get_db), current_user: schemas.UserModel = Depends(oauth2.get_current_user)):
    
    # post= db.query(models.Post).filter(models.Post.id==id).first()
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True
        ).group_by(models.Post.id).filter(models.Post.id==id, models.Post.user_id == current_user.id ).first()

    if not post:
        # return ORJSONResponse(
        #     {"error":"post with id: {id} does not exist for this user"},
        #      status_code=status.HTTP_404_NOT_FOUND
        # )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist for this user") 
    # print(post)
                            
    # if post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                     detail=f"Unauthorized used") 
    return post



@router.post("/", status_code=status.HTTP_201_CREATED , response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.UserModel = Depends(oauth2.get_current_user)):
    # post= pos.dict()
    # post= db.query(models.Post).all()
    # post.
    # post_new=  models.Post(title = post.title, content = post.content, published = post.published)
    print("current_user", current_user.email)
    post_new=  models.Post(user_id=current_user.id, **post.model_dump())
    db.add(post_new)
    db.commit()
    db.refresh(post_new)
    return post_new
# {"post": post_new, "user": current_user.email}

@router.put("/{id}")
def update_posts(id:int, post:schemas.PostCreate,  db: Session = Depends(get_db), current_user: schemas.UserModel = Depends(oauth2.get_current_user)):
    post_qry= db.query(models.Post).filter(models.Post.id==id)
    post = post_qry.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Unauthorized used")    
    

    post_qry.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_qry.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def create_posts(id: int, db: Session = Depends(get_db), current_user: schemas.UserModel = Depends(oauth2.get_current_user)):
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Unauthorized used")    

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

