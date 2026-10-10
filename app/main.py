
from fastapi import FastAPI
from dotenv import load_dotenv
from . import models
from .database import engine
from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/")
async def read_root():
    return {"Hello": "World"}


