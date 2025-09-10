from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Common base for user-related schemas
class UserBase(BaseModel):
    username: str
    email: str
    name: str


# Schema for creating a new user
class UserCreate(UserBase):
    password: str


# Schema for updating user information
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None


# Schema representing a user in the database (for internal use)
class UserInDB(UserBase):
    user_id: int
    password: str  # Stored hashed password
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# Schema for reading user data (sent to client)
class UserRead(UserBase):
    user_id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# Simple schema for relationships
class UserSimple(BaseModel):
    user_id: int
    username: str

    class Config:
        from_attributes = True
