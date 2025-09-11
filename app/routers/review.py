from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.schemas.review import ReviewRead, ReviewCreate
from app.services.review_service import ReviewService
from app.db.models.user import User
from app.middlewares.authentication import get_current_user

router = APIRouter()


async def get_review_service(db: AsyncSession = Depends(get_db)) -> ReviewService:
    return ReviewService(db)


@router.post("/", response_model=ReviewRead)
async def create_review(
    review: ReviewCreate, 
    review_service: ReviewService = Depends(get_review_service),
    current_user: User = Depends(get_current_user)
):
    return await review_service.create_review(review=review, user_id=current_user.user_id)


@router.get("/product/{product_id}", response_model=List[ReviewRead])
async def read_reviews_for_product(
    product_id: int, skip: int = 0, limit: int = 100, review_service: ReviewService = Depends(get_review_service)
):
    reviews = await review_service.get_reviews_by_product(
        product_id=product_id, skip=skip, limit=limit
    )
    return reviews


@router.get("/{review_id}", response_model=ReviewRead)
async def read_review(
    review_id: int, review_service: ReviewService = Depends(get_review_service)
):
    db_review = await review_service.get_review(review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review


@router.delete("/{review_id}", response_model=ReviewRead)
async def delete_review(
    review_id: int, review_service: ReviewService = Depends(get_review_service)
):
    db_review = await review_service.delete_review(review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review