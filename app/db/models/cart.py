from __future__ import annotations
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, Table, Column, Numeric
from typing import List

from app.db.models.product import Product

# Association Table for the many-to-many relationship between Cart and Product
cart_item_association = Table(
    "cart_item_association",
    Base.metadata,
    Column("cart_id", ForeignKey("cart.cart_id"), primary_key=True),
    Column("product_id", ForeignKey("product.product_id"), primary_key=True),
    Column("quantity", Integer, default=1, nullable=False),
)


class Cart(Base):
    __tablename__ = "cart"

    cart_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Foreign Key for one-to-one relationship
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), unique=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="cart")
    products: Mapped[List["Product"]] = relationship(
        secondary=cart_item_association, back_populates="carts"
    )