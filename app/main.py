import psycopg2
import time
import os
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, Response, status
from dotenv import load_dotenv
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from .schemas import PostCreate, Post, UserCreate, User

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


