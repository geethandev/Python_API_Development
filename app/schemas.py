from typing import Optional, Union
from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class ResponsePost(PostBase):
    id: int
    created_at: datetime
    user_id: int
    class Config:  
        orm_mode = True

  
        
class CreateUser(BaseModel):
    Email: EmailStr
    password: str
    
    
class UserLogin(BaseModel):
        Email: EmailStr
        password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    