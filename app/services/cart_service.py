from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import cart as cart_repository
from app.schemas.cart import CartItemAdd
from app.db.models.cart import Cart
from typing import Optional


class CartService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_cart_by_user_id(self, user_id: int) -> Optional[Cart]:
        return await cart_repository.get_cart_by_user_id(self.db, user_id)

    async def add_item_to_cart(self, user_id: int, item: CartItemAdd) -> Cart:
        return await cart_repository.add_item_to_cart(self.db, user_id, item)

    async def remove_item_from_cart(self, user_id: int, product_id: int) -> Optional[Cart]:
        return await cart_repository.remove_item_from_cart(self.db, user_id, product_id)