from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models.product import Product
from app.schemas.product import ProductCreate
from typing import Optional, List


async def get_product(db: AsyncSession, product_id: int) -> Optional[Product]:
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.reviews))
        .filter(Product.product_id == product_id)
    )
    return result.scalars().first()


async def get_products(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[Product]:
    result = await db.execute(
        select(Product).options(selectinload(Product.reviews)).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_product(db: AsyncSession, product: ProductCreate) -> Product:
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    # Re-query to load the relationship
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.reviews))
        .filter(Product.product_id == db_product.product_id)
    )
    return result.scalars().one()


async def update_product(
    db: AsyncSession, product_id: int, product_update: ProductCreate
) -> Optional[Product]:
    db_product = await get_product(db, product_id)
    if db_product:
        update_data = product_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        await db.commit()
        await db.refresh(db_product)
        # Re-query to load the relationship
        result = await db.execute(
            select(Product)
            .options(selectinload(Product.reviews))
            .filter(Product.product_id == db_product.product_id)
        )
        return result.scalars().one()
    return db_product


async def delete_product(db: AsyncSession, product_id: int) -> Optional[Product]:
    db_product = await get_product(db, product_id)
    if db_product:
        await db.delete(db_product)
        await db.commit()
    return db_product