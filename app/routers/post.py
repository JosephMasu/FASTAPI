from . . import models, schemas
from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from . .database import engine, get_db

router = APIRouter(
    prefix="/api/v1/posts",
    tags=["Posts"]
)

@router.get("/sqlalchemy", status_code=status.HTTP_200_OK, response_model=list[schemas.Post])
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts

@router.post("/sqlalchemy", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = models.Post(**new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return  post

@router.get("/latest/sqlalchemy")
def get_latest_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    db.close()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no posts found",
        )
    return post

@router.get("/slqalchemy/{id}", response_model=schemas.Post)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    db.close()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return post

@router.delete("/slqalchemy/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/slqalchemy/{id}", response_model=schemas.Post) 
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