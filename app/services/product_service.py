from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import product as product_repository
from app.schemas.product import ProductCreate
from app.db.models.product import Product
from typing import Optional, List


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_product(self, product: ProductCreate) -> Product:
        return await product_repository.create_product(self.db, product)

    async def get_product(self, product_id: int) -> Optional[Product]:
        return await product_repository.get_product(self.db, product_id)

    async def get_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return await product_repository.get_products(self.db, skip, limit)

    async def update_product(
        self, product_id: int, product_update: ProductCreate
    ) -> Optional[Product]:
        return await product_repository.update_product(self.db, product_id, product_update)

    async def delete_product(self, product_id: int) -> Optional[Product]:
        return await product_repository.delete_product(self.db, product_id)