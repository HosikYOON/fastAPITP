from pydantic import BaseModel
from typing import List
from decimal import Decimal
from . import user, product


# Schema for adding an item to the cart
class CartItemAdd(BaseModel):
    product_id: int
    quantity: int


# Schema for reading cart data
class CartRead(BaseModel):
    cart_id: int
    user: user.UserSimple
    products: List[product.ProductSimple] = []  # Simplified

    class Config:
        from_attributes = True
