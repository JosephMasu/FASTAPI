import psycopg2
import time
import os
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, Response, status
from dotenv import load_dotenv
from . import models, schemas;
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from .schemas import PostCreate 

models.Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST"),
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            port=os.getenv("DATABASE_PORT"),
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        
        print("Database connection was successful")
        break

    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        time.sleep(2)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/api/v1/posts/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts

@app.post("/api/v1/posts/sqlalchemy", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = models.Post(**new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return  post

@app.get("/api/v1/posts/latest/sqlalchemy")
def get_latest_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    db.close()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no posts found",
        )
    return post

@app.get("/api/v1/posts/slqalchemy/{id}")
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    db.close()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return post

@app.delete("/api/v1/posts/slqalchemy/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db:Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    post = deleted_post.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/api/v1/posts/slqalchemy/{id}")
def update_post_by_id(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    db_post = post_query.first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return db_post
