from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional, List

from app.core.security import get_password_hash


async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).filter(User.user_id == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        name=user.name,
        password=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(
    db: AsyncSession, user_id: int, user_update: UserUpdate
) -> Optional[User]:
    db_user = await get_user(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])
        for key, value in update_data.items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int) -> Optional[User]:
    db_user = await get_user(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user
