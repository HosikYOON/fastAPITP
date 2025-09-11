from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.schemas.user import UserRead, UserCreate, UserUpdate, Token
from app.services.user_service import UserService
from app.core.security import create_access_token
from app.db.models.user import User
from app.middlewares.authentication import get_current_user

router = APIRouter()


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/", response_model=UserRead)
async def create_user(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
):
    db_user = await user_service.create_user(user=user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user


@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=List[UserRead])
async def read_users(
    skip: int = 0, limit: int = 100, user_service: UserService = Depends(get_user_service)
):
    users = await user_service.get_users(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    db_user = await user_service.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int, user: UserUpdate, user_service: UserService = Depends(get_user_service)
):
    db_user = await user_service.update_user(user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    db_user = await user_service.delete_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user