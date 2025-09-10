from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, ForeignKey, TIMESTAMP, func
from typing import Optional
from datetime import datetime


class Review(Base):
    __tablename__ = "review"

    review_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(Text)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=True
    )

    # Foreign Keys
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), nullable=False)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.product_id"), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="reviews")
    product: Mapped["Product"] = relationship(back_populates="reviews")
