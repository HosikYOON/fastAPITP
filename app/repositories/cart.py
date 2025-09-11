from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from app.db.models.cart import Cart, cart_item_association
from app.db.models.product import Product
from app.schemas.cart import CartItemAdd
from typing import Optional


async def get_cart_by_user_id(db: AsyncSession, user_id: int) -> Optional[Cart]:
    result = await db.execute(select(Cart).filter(Cart.user_id == user_id))
    return result.scalars().first()


async def add_item_to_cart(db: AsyncSession, user_id: int, item: CartItemAdd) -> Cart:
    cart = await get_cart_by_user_id(db, user_id)
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        await db.commit()
        await db.refresh(cart)

    product = await db.execute(select(Product).filter(Product.product_id == item.product_id))
    product = product.scalars().first()
    if not product:
        # Or raise an exception
        return None

    # Check if the item is already in the cart
    cart_item_result = await db.execute(
        select(cart_item_association)
        .filter_by(cart_id=cart.cart_id, product_id=item.product_id)
    )
    cart_item = cart_item_result.first()

    if cart_item:
        # Update quantity
        update_stmt = (
            update(cart_item_association)
            .where(cart_item_association.c.cart_id == cart.cart_id)
            .where(cart_item_association.c.product_id == item.product_id)
            .values(quantity=cart_item.quantity + item.quantity)
        )
        await db.execute(update_stmt)
    else:
        # Add new item
        insert_stmt = insert(cart_item_association).values(
            cart_id=cart.cart_id, product_id=item.product_id, quantity=item.quantity
        )
        await db.execute(insert_stmt)

    await db.commit()
    await db.refresh(cart)
    return cart


async def remove_item_from_cart(db: AsyncSession, user_id: int, product_id: int) -> Optional[Cart]:
    cart = await get_cart_by_user_id(db, user_id)
    if not cart:
        return None

    # Check if the item is in the cart
    cart_item_result = await db.execute(
        select(cart_item_association)
        .filter_by(cart_id=cart.cart_id, product_id=product_id)
    )
    cart_item = cart_item_result.first()

    if cart_item:
        # Remove the item
        delete_stmt = (
            delete(cart_item_association)
            .where(cart_item_association.c.cart_id == cart.cart_id)
            .where(cart_item_association.c.product_id == product_id)
        )
        await db.execute(delete_stmt)
        await db.commit()
        await db.refresh(cart)

    return cart
