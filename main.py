from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/api/v1/posts")
def get_post():
    return {"message": "This is a POST request"}
    
@app.post("/api/v1/posts")
def post_post():
    return {"message": "first post created"}