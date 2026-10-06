from . . import models, schemas, utils
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from . .database import engine, get_db

router = APIRouter()

@router.post("/api/v1/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/api/v1/users/{id}", response_model=schemas.User)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    db.close()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found",
        )
    return user