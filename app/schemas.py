from pydantic import BaseModel
from datetime import datetime 

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    title: str
    content: str
    published: bool = True
    created_at: datetime

    class Config:
        orm_mode = True

