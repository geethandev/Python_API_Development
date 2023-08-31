
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..import models, schemas
from ..routers import auth
from ..database import get_db

router = APIRouter(
    prefix = '/posts',
    tags=['posts']
)

@router.get("/",response_model = List[schemas.ResponsePost])
async def get_post(db: Session = Depends(get_db),Current_user: int = Depends(auth.get_current_user),limit:int = 5):
    try:
        print(limit)
        posts = db.query(models.Post).limit(limit).all()
        return  posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
async def create_post(post: schemas.PostBase, db: Session = Depends(get_db), Current_user: int = Depends(auth.get_current_user)):
    try:
        new_post = models.Post(**post.dict(), user_id=Current_user)  # Assign user_id
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
@router.get("/latest",response_model = list[schemas.ResponsePost])
async def latest(db: Session = Depends(get_db),Current_user:int = Depends(auth.get_current_user)):
      # Endpoint to get the latest post
    try:
        post = db.query(models.Post).limit(3).all()
        return post
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
      
    
@router.get("/{id}", response_model=schemas.ResponsePost)
async def get_id(id: int, db: Session = Depends(get_db), Current_user: int = Depends(auth.get_current_user)):
    try:
        # Use filter with .first() to get a single post by its ID
        post = db.query(models.Post).filter(models.Post.id == id).first()
        
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
 
        return post

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    
@router.put("/{id}", response_model=schemas.ResponsePost)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), Current_user: int = Depends(auth.get_current_user)):

    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()

        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id Not Found')
        
        if post.user_id != Current_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this post")

        # Use dict.update() to efficiently update the post attributes from the updated_post
        post_dict = updated_post.dict(exclude_unset=True)
        for key, value in post_dict.items():
            setattr(post, key, value)

        db.commit() 
        db.refresh(post)  # Refresh the post to reflect the updated values

        return post 

    except HTTPException as http_exception:
        raise HTTPException(
            status_code=http_exception.status_code,
            detail=f"Error updating post: {http_exception.detail}"
        )

    except Exception as e:
        # Return a 500 Internal Server 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating post: {str(e)}"
        )





@router.delete("/{id}")
async def delete_post(id: int, db: Session = Depends(get_db), Current_user: int = Depends(auth.get_current_user)):

    try:
        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.first()

        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post Not Found')
        
        if post.user_id != Current_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this post")

        post_query.delete(synchronize_session=False)
        db.commit()

        return {'message': 'Post deleted successfully'}

    except HTTPException as http_exception:
        # Return the raised HTTPException with a custom detail message
        raise HTTPException(
            status_code=http_exception.status_code,
            detail=f"Error deleting post: {http_exception.detail}"
        )

    except Exception as e:
        # Return a 500 Internal Server Error with a custom detail message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting post: {str(e)}"
        )

    
    
    