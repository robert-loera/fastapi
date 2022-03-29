# these are schemas to make sure the user can only
# pass and retreive certain defined info
from typing import Optional
from venv import create
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from app.database import Base


class PostBase(BaseModel):
    title: str
    content: str
    # if user doesnt pass published value default is True
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    # inherits the rest from the other class
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    # created_at
    # this is boiler plate needed for return schemas

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    # conint allows us to specify the user can only put 1 or less than for like = 1 unlike = 0
    dir: conint(le=1)
