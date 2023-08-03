
from fastapi import (Depends, FastAPI, Form, HTTPException, Request, Response,
                     status)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from .database import engine, get_db
from .models import Post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")



@app.get("/")
async def root():
    return {"message": "Root"}


''' CURD OPERATION STARTS ''' # Completed 
@app.get("/posts",response_model = schemas.ResponsePost)
async def get_post(db: Session = Depends(get_db)):
    try:
        posts = db.query(models.Post).all()
        return  posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model = schemas.ResponsePost)
async def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
    try:  
        new_post = models.Post(**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
@app.get("/posts/latest",response_model = list[schemas.ResponsePost])
async def latest(db: Session = Depends(get_db)):
      # Endpoint to get the latest post
    try:
        post = db.query(models.Post).limit(3).all()
        return post
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
      
    
@app.get("/posts/{id}",response_model=schemas.ResponsePost)
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

    
    
@app.put("/posts/{id}",response_model = schemas.ResponsePost)
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



@app.delete("/posts/{id}")
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

    
    
# ''' CURD OPERATION ENDS '''   

# ----------------------------------------------------------------------------------------------------------------------

# Create user


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    try:
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {'message': 'User created'}

    except IntegrityError as e:
        # Check if the error is related to the uniqueness constraint violation on the 'Email' column
        if "UNIQUE KEY constraint" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists. Please use another email.')
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))