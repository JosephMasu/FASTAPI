from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/api/v1/posts")
def get_post():
    return {"message": "This is a POST request"}
    
@app.post("/api/v1/posts")
def post_post(payload: dict = Body(...)):
    print(payload)
    return {"message": f"title: {payload['title']}, content: {payload['content']}"}
