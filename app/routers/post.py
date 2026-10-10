from .. import models, schemas, oauth2
from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional


router = APIRouter(
    prefix="/api/v1/posts",
    tags=["Posts"]
)

def posts_with_votes(db: Session):
    return db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id)

@router.get("/sqlalchemy", status_code=status.HTTP_200_OK, response_model=list[schemas.PostOut])
def test_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), 
                limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    return posts_with_votes(db).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

@router.post("/sqlalchemy", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    print(current_user.email)
    post = models.Post(owner_id = current_user.id, **new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return  post

@router.get("/latest/sqlalchemy", response_model=schemas.PostOut)
def get_latest_post(db: Session = Depends(get_db)):
    post = posts_with_votes(db).order_by(models.Post.id.desc()).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no posts found",
        )
    return post

@router.get("/slqalchemy/{id}", response_model=schemas.PostOut)
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = posts_with_votes(db).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    if post.Post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    return post

@router.delete("/slqalchemy/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db:Session = Depends(get_db), current_user: models.User = Depends(
    oauth2.get_current_user)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    post = deleted_post.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  
            detail="Not authorized to perform requested action",
        )

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/slqalchemy/{id}", response_model=schemas.Post) 
def update_post_by_id(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), 
                      current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    db_post = post_query.first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    
    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  
            detail="Not authorized to perform requested action",
        )
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return db_post