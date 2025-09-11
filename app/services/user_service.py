from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import user as user_repository
from app.schemas.user import UserCreate, UserUpdate
from app.db.models.user import User
from app.core.security import get_password_hash, verify_password
from typing import Optional, List


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: UserCreate) -> Optional[User]:
        db_user = await user_repository.get_user_by_email(self.db, email=user.email)
        if db_user:
            return None  # Or raise an exception
        return await user_repository.create_user(self.db, user=user)

    async def get_user(self, user_id: int) -> Optional[User]:
        return await user_repository.get_user(self.db, user_id)

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await user_repository.get_users(self.db, skip, limit)

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        return await user_repository.update_user(self.db, user_id, user_update)

    async def delete_user(self, user_id: int) -> Optional[User]:
        return await user_repository.delete_user(self.db, user_id)

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await user_repository.get_user_by_username(self.db, username=username)
        if not user or not verify_password(password, user.password):
            return None
        return user