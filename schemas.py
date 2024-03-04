from pydantic import BaseModel, ValidationError, field_serializer, EmailStr
from datetime import datetime, timezone
from typing import Optional

class UserModel(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: str
    id: int
    created_at: datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass



class PostResponse(PostBase):
    id:int
    created_at: datetime
    user_id:int
    user: UserResponse

    # @field_serializer('created_at')
    # def serialize_dt(self, created_at: datetime, _info):
    #     return created_at.timestamp()

    class Config:
        orm_model=True


class PostVoteResponse(BaseModel):
    Post: PostResponse
    votes:int

    class Config:
        orm_model=True


class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id:Optional[int]=None

class Vote(BaseModel):
    post_id:int
    dir:int

