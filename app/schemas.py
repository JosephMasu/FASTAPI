from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime 
from typing import Optional, Annotated
from pydantic import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class User(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User

    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    post: Post = Field(validation_alias="Post")
    votes: int

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, conint(ge=0, le=1)]