from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 3}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/api/v1/posts")
def get_post():
    return {"data": my_posts}
    
@app.post("/api/v1/posts", status_code=status.HTTP_201_CREATED)
def post_post(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(new_post.dict())
    return {"data": post_dict}

@app.get("/api/v1/posts/latest")
def get_latest_byId():
    post = my_posts[len(my_posts)-1]
    return {"latest_post": post}

@app.get("/api/v1/posts/{id}")
def get_post_byId(id:int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    print(post)
    return {"post_detail": post}

@app.delete("/api/v1/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_byId(id:int, post: Post):
    # post = find_post(id)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # my_posts.remove(post)
    # return Response(status_code=status.HTTP_204_NO_CONTENT
    
    index = find_post_index(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )
    my_posts.pop(index)

    return {"data": f"post with id: {id} was successfully updated"}


@app.put("/api/v1/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post_byId(id:int, post: Post):
    # post = find_post(id)
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # my_posts.remove(post)
    # return Response(status_code=status.HTTP_204_NO_CONTENT
    
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"data": post_dict}
