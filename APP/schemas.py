from pydantic import BaseModel, EmailStr, conint

from typing import Optional

from datetime import datetime



# Create User
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Return create user response
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True



# It validates that the request has all the fields and of proper type
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# Return respose structure
class PostResponse(PostBase):
    id: int
    owner: User
    created_at: datetime

    class Config:
        from_attributes = True


class PostVote(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True



# Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None



# Vote
class Vote(BaseModel):
    post_id: int
    dir: conint(le = 1)