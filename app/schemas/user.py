from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# 베이스 모델
class UserBase(BaseModel):
    username: str
    email: str
    name: str


# 회원가입용
class UserCreate(UserBase):
    password: str


# 회원 정보 수장
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None


# 내부 사용용
class UserInDB(UserBase):
    user_id: int
    password: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# 유저 정보 읽어오기
class UserRead(UserBase):
    user_id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# Foreign Key 용 간단한 데이터베이스
class UserSimple(BaseModel):
    user_id: int
    username: str

    class Config:
        from_attributes = True
