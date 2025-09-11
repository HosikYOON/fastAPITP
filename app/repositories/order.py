from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from app.db.models.order import Order, order_product_association
from app.db.models.product import Product
from app.db.models.cart import Cart
from typing import Optional, List
from decimal import Decimal


async def get_order(db: AsyncSession, order_id: int) -> Optional[Order]:
    result = await db.execute(select(Order).filter(Order.order_id == order_id))
    return result.scalars().first()


async def get_orders_by_user(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
) -> List[Order]:
    result = await db.execute(select(Order).filter(Order.user_id == user_id).offset(skip).limit(limit))
    return result.scalars().all()


async def create_order_from_cart(db: AsyncSession, user_id: int) -> Optional[Order]:
    cart_result = await db.execute(select(Cart).filter(Cart.user_id == user_id))
    cart = cart_result.scalars().first()
    if not cart or not cart.products:
        return None  # Cart is empty or doesn't exist

    total_amount = Decimal(0)
    order_products = []

    for cart_item in cart.products:
        product_result = await db.execute(select(Product).filter(Product.product_id == cart_item.product_id))
        product = product_result.scalars().first()
        quantity = cart_item.quantity
        price_at_purchase = product.price

        if product.stock_quantity < quantity:
            # Not enough stock
            # You might want to raise an exception here
            return None

        total_amount += price_at_purchase * quantity
        product.stock_quantity -= quantity

        order_products.append(
            {
                "product_id": product.product_id,
                "quantity": quantity,
                "price_at_purchase": price_at_purchase,
            }
        )

    # Create the order
    db_order = Order(user_id=user_id, total_amount=total_amount)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    # Add products to the order
    for item in order_products:
        insert_stmt = insert(order_product_association).values(
            order_id=db_order.order_id, **item
        )
        await db.execute(insert_stmt)

    # Clear the cart
    await db.execute(delete(Cart).filter(Cart.user_id == user_id))

    await db.commit()
    await db.refresh(db_order)

    return db_order
