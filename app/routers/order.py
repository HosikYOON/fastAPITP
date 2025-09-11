from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.schemas.order import OrderRead
from app.services.order_service import OrderService

router = APIRouter()


async def get_order_service(db: AsyncSession = Depends(get_db)) -> OrderService:
    return OrderService(db)


@router.post("/from_cart/{user_id}", response_model=OrderRead)
async def create_order_from_cart(
    user_id: int, order_service: OrderService = Depends(get_order_service)
):
    order = await order_service.create_order_from_cart(user_id=user_id)
    if order is None:
        raise HTTPException(
            status_code=400, detail="Cart is empty or product is out of stock"
        )
    return order


@router.get("/{order_id}", response_model=OrderRead)
async def read_order(
    order_id: int, order_service: OrderService = Depends(get_order_service)
):
    db_order = await order_service.get_order(order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.get("/user/{user_id}", response_model=List[OrderRead])
async def read_orders_for_user(
    user_id: int, skip: int = 0, limit: int = 100, order_service: OrderService = Depends(get_order_service)
):
    orders = await order_service.get_orders_by_user(
        user_id=user_id, skip=skip, limit=limit
    )
    return orders
