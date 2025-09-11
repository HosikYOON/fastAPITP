from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal

# Schema for creating or updating a product
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    stock_quantity: int


# Schema for reading product data
class ProductRead(BaseModel):
    product_id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    stock_quantity: int
    reviews: List[ReviewRead] = []

    class Config:
        from_attributes = True


# Simple schema for use in nested relationships
class ProductSimple(BaseModel):
    product_id: int
    name: str
    price: Decimal

    class Config:
        from_attributes = True