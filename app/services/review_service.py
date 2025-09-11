from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import review as review_repository
from app.schemas.review import ReviewCreate
from app.db.models.review import Review
from typing import Optional, List


class ReviewService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_review(self, review: ReviewCreate) -> Review:
        return await review_repository.create_review(self.db, review)

    async def get_review(self, review_id: int) -> Optional[Review]:
        return await review_repository.get_review(self.db, review_id)

    async def get_reviews_by_product(
        self, product_id: int, skip: int = 0, limit: int = 100
    ) -> List[Review]:
        return await review_repository.get_reviews_by_product(self.db, product_id, skip, limit)

    async def delete_review(self, review_id: int) -> Optional[Review]:
        return await review_repository.delete_review(self.db, review_id)