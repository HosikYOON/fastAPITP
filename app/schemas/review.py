from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from . import user # Import related schemas


# Schema for creating a new review
class ReviewCreate(BaseModel):
    rating: int
    comment: str
    product_id: int


# Schema for reading review data, including nested relationships
class ReviewRead(BaseModel):
    review_id: int
    rating: int
    comment: str
    created_at: Optional[datetime]
    user: user.UserSimple  # Nested user schema
    product: ProductSimple  # Nested product schema

    class Config:
        from_attributes = True