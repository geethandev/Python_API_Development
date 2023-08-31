from datetime import datetime, timedelta
from config import settings

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .. import models, schemas, utils,main
from ..database import get_db

router = APIRouter(
    tags=['authentication']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Getting from Config file 
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def Access_Token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode["exp"] = expire  # Adding the expiration time to the dictionary
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_Token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: str = payload.get('user_id')
        
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
        return token_data
    except JWTError:
        raise credentials_exception
        

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_Token(token, credentials_exception)
    
    user_id = token_data.id
    return user_id


# --------------------------------------------------------------------------------------------------------------------------------



@router.post('/login/')
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) :

        user = db.query(models.User).filter(models.User.Email == user_credentials.username).first()
 
         
        if not user:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User Not Found')

        if not utils.verify(user_credentials.password, user.password):
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='incorrect password')

        
        token = Access_Token(data={"user_id": user.id})
        
        return {"token": token, "token_type": "Bearer"}

