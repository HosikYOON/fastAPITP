from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models.review import Review
from app.schemas.review import ReviewCreate
from typing import Optional, List


async def get_review(db: AsyncSession, review_id: int) -> Optional[Review]:
    result = await db.execute(
        select(Review)
        .options(selectinload(Review.user), selectinload(Review.product))
        .filter(Review.review_id == review_id)
    )
    return result.scalars().first()


async def get_reviews_by_product(
    db: AsyncSession, product_id: int, skip: int = 0, limit: int = 100
) -> List[Review]:
    result = await db.execute(
        select(Review)
        .options(selectinload(Review.user), selectinload(Review.product))
        .filter(Review.product_id == product_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_review(db: AsyncSession, review: ReviewCreate, user_id: int) -> Review:
    db_review = Review(**review.model_dump(), user_id=user_id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    # Re-query to load relationships
    result = await db.execute(
        select(Review)
        .options(selectinload(Review.user), selectinload(Review.product))
        .filter(Review.review_id == db_review.review_id)
    )
    return result.scalars().one()


async def delete_review(db: AsyncSession, review_id: int) -> Optional[Review]:
    db_review = await get_review(db, review_id)
    if db_review:
        await db.delete(db_review)
        await db.commit()
    return db_review