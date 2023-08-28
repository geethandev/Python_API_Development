from fastapi import Depends,APIRouter,status,HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from..database import get_db
from..import schemas,utils
router = APIRouter(
    tags=['authentication']
)


@router.post('/login/')
def login(user_credentials:schemas.UserLogin, db: Session = Depends(get_db)) :

        user = db.query(models.User).filter(models.User.Email == user_credentials.Email).first()
 
         
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User Not Found')
        
        if not utils.verify(user_credentials.password,user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='incorrect password')
        return {'token':"success"}

