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
    class Config:
        orm_mode = True

  
        
class CreateUser(BaseModel):
    Email: EmailStr
    password: str
    