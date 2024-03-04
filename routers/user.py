


from sqlalchemy.orm import Session
from database import engine , get_db
from fastapi import FastAPI, Query, Response, status, HTTPException, Depends , APIRouter
import models, schemas, utils

router=APIRouter(
    prefix="/user",
    tags=["Users endpoint"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user:schemas.UserModel, db: Session = Depends(get_db)):
    hashed_pass=utils.hash(user.password)
    user.password=hashed_pass

    new_user=  models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id:int, db: Session = Depends(get_db)):
    user= db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    return user