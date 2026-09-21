from typing import Optional
from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/api/v1/posts")
def get_post():
    return {"message": "This is a POST request"}
    
@app.post("/api/v1/posts")
def post_post(new_post: Post):
    print(new_post)
    return {"data": new_post}
