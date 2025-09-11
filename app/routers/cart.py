from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.cart import CartRead, CartItemAdd
from app.services.cart_service import CartService

router = APIRouter()


async def get_cart_service(db: AsyncSession = Depends(get_db)) -> CartService:
    return CartService(db)


@router.get("/{user_id}", response_model=CartRead)
async def read_cart(
    user_id: int, cart_service: CartService = Depends(get_cart_service)
):
    cart = await cart_service.get_cart_by_user_id(user_id=user_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("/{user_id}/items", response_model=CartRead)
async def add_to_cart(
    user_id: int, item: CartItemAdd, cart_service: CartService = Depends(get_cart_service)
):
    cart = await cart_service.add_item_to_cart(user_id=user_id, item=item)
    if cart is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return cart


@router.delete("/{user_id}/items/{product_id}", response_model=CartRead)
async def remove_from_cart(
    user_id: int, product_id: int, cart_service: CartService = Depends(get_cart_service)
):
    cart = await cart_service.remove_item_from_cart(
        user_id=user_id, product_id=product_id
    )
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart
