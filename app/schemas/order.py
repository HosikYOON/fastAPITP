from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from . import user, product  # Import related schemas


# Schema for creating an order
class OrderCreate(BaseModel):
    user_id: int
    # You would typically pass a list of items and quantities here
    # For example: items: List[dict]


# Schema for reading order data
class OrderRead(BaseModel):
    order_id: int
    status: str
    total_amount: Decimal
    created_at: Optional[datetime]
    user: user.UserSimple
    products: List[product.ProductSimple] = []  # Note: This is simplified

    class Config:
        from_attributes = True
