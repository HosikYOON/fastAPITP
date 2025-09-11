from __future__ import annotations
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer,
    String,
    TIMESTAMP,
    func,
    ForeignKey,
    Table,
    Column,
    Numeric,
)
from typing import Optional, List
from datetime import datetime

from app.db.models.product import Product

# Association Table for the many-to-many relationship between Order and Product
order_product_association = Table(
    "order_product_association",
    Base.metadata,
    Column("order_id", ForeignKey("order.order_id"), primary_key=True),
    Column("product_id", ForeignKey("product.product_id"), primary_key=True),
    Column("quantity", Integer, default=1, nullable=False),
    Column("price_at_purchase", Numeric(10, 2), nullable=False),
)


class Order(Base):
    __tablename__ = "order"

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    total_amount: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=True
    )

    # Foreign Key
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="orders")
    products: Mapped[List["Product"]] = relationship(
        secondary=order_product_association, back_populates="orders"
    )