from __future__ import annotations
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func
from typing import Optional, List


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    password: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=True
    )

    # Relationships
    reviews: Mapped[List["Review"]] = relationship(back_populates="user")
    orders: Mapped[List["Order"]] = relationship(back_populates="user")
    cart: Mapped["Cart"] = relationship(back_populates="user")
