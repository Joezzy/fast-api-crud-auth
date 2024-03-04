from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas, database, models
from sqlalchemy.orm import Session
from config import settings



oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY=settings.SECRET_KEY
ALGOITHM=settings.ALGORITHM
TOKEN__EXPIRY_MINUTES=settings.ACCESS_TOKEN_EXPIRRY


def  create_access_token(data:dict):
    to_encode=data.copy()

    expire=datetime.utcnow() + timedelta(minutes=TOKEN__EXPIRY_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGOITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGOITHM])

        id :str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        print("USER_ID",id)
        token_data=schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception 
    
    return token_data
    

def get_current_user(token:str =Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                       detail=f"Could not validate credentials",headers={"WWW-Authenticate": "Bearer"} )
  
    token= verify_access_token(token,credential_exception)
    print("USER_ID-T",token.id)

    user = db.query(models.User).filter(models.User.id  == token.id).first()
    print(user.id)
    print(user.email)


    return user
