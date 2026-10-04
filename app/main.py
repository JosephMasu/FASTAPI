import psycopg2
import time
import os
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from dotenv import load_dotenv
from . import models;
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/api/v1/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts ORDER BY id")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/api/v1/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (new_post.title, new_post.content, new_post.published),
    )
    created_post = cursor.fetchone()
    conn.commit()
    return {"data": created_post}

@app.get("/api/v1/posts/latest")
def get_latest_post():
    cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no posts found",
        )
    return {"latest_post": post}

@app.get("/api/v1/posts/{id}")
def get_post_by_id(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"data": post}

@app.delete("/api/v1/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/api/v1/posts/{id}")
def update_post_by_id(id: int, post: Post):
    cursor.execute(
        """
        UPDATE posts
        SET title = %s, content = %s, published = %s, updated_at = now()
        WHERE id = %s
        RETURNING *
        """,
        (post.title, post.content, post.published, id),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"data": updated_post}
