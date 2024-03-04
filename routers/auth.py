
from sqlalchemy.orm import Session
from database import engine , get_db
from fastapi import FastAPI, Query, Response, status, HTTPException, Depends , APIRouter
import models, schemas, utils
import oauth2
router=APIRouter(
    prefix="/auth",
    tags=["Users endpoint"]
)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user:schemas.UserModel, db: Session = Depends(get_db)):

    user_rec= db.query(models.User).filter(models.User.email==user.email).first()

    if not user_rec:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credential")


    if not  utils.verifyPassword(user.password, user_rec.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credential")
    
    access_token=oauth2.create_access_token(data={"user_id":user_rec.id})
    return {"token":access_token, "data":user_rec}

