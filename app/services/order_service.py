from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import order as order_repository
from app.db.models.order import Order
from typing import Optional, List


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_order(self, order_id: int) -> Optional[Order]:
        return await order_repository.get_order(self.db, order_id)

    async def get_orders_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return await order_repository.get_orders_by_user(self.db, user_id, skip, limit)

    async def create_order_from_cart(self, user_id: int) -> Optional[Order]:
        return await order_repository.create_order_from_cart(self.db, user_id)