from sqlalchemy import Boolean, Column, DateTime, Integer, String, func, text

from .database import Base


# For all Posts related table
class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

# For User Table
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Email = Column(String(255), nullable=False,unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now()) 