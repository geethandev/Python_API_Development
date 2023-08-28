
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..import models, schemas
from ..database import get_db

router = APIRouter(
    prefix = '/posts',
    tags=['posts']
)

@router.get("/",response_model = List[schemas.ResponsePost])
async def get_post(db: Session = Depends(get_db)):
    try:
        posts = db.query(models.Post).all()
        return  posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/",status_code=status.HTTP_201_CREATED,response_model = schemas.ResponsePost)
async def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
    try:  
        new_post = models.Post(**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
@router.get("/latest",response_model = list[schemas.ResponsePost])
async def latest(db: Session = Depends(get_db)):
      # Endpoint to get the latest post
    try:
        post = db.query(models.Post).limit(3).all()
        return post
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
      
    
@router.get("/{id}",response_model=schemas.ResponsePost)
async def get_id(id: int, db: Session = Depends(get_db)):
    try:
        # Use filter with .first() to get a single post by its ID
        post = db.query(models.Post).filter(models.Post.id == id).first()
        
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')

        # Return the post data in the expected format of schemas.ResponsePost
        return post

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    
    
@router.put("/{id}",response_model = schemas.ResponsePost)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()

        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id Not Found')

        # Use dict.update() to efficiently update the post attributes from the updated_post
        post_dict = updated_post.dict(exclude_unset=True)
        for key, value in post_dict.items():
            setattr(post, key, value)

        db.commit() 
        db.refresh(post)  # Refresh the post to reflect the updated values

        return post

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error updating post')



@router.delete("/{id}")
async def delete_post(id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()

        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')

        db.delete(post)
        db.commit()

        return {'message': 'Post deleted successfully'}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error deleting post')