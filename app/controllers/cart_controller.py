from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product_variant import ProductVariant
from app.models.price import Price


async def get_or_create_cart(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Cart).where(Cart.user_id == user_id)
    )
    cart = result.scalar_one_or_none()

    if cart:
        return cart

    cart = Cart(user_id=user_id)
    db.add(cart)
    await db.flush()
    return cart


async def add_item_to_cart(db: AsyncSession, user_id: int, variant_id: int, quantity: int):
    async with db.begin():
        variant = await db.get(ProductVariant, variant_id)
        if not variant:
            return {"error": "Variant does not exist"}

        cart = await get_or_create_cart(db, user_id)

        result = await db.execute(
            select(CartItem).where(
                CartItem.cart_id == cart.id,
                CartItem.variant_id == variant_id
            )
        )
        item = result.scalar_one_or_none()

        if item:
            item.quantity += quantity
        else:
            db.add(
                CartItem(
                    cart_id=cart.id,
                    variant_id=variant_id,
                    quantity=quantity
                )
            )

    return {"message": "Item added to cart"}


async def update_cart_item(db: AsyncSession, item_id: int, quantity: int):
    async with db.begin():
        item = await db.get(CartItem, item_id)
        if not item:
            return None

        item.quantity = quantity
    return item


async def remove_cart_item(db: AsyncSession, item_id: int):
    async with db.begin():
        item = await db.get(CartItem, item_id)
        if not item:
            return None

        await db.delete(item)
    return {"message": "Item removed"}


async def get_cart(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Cart).where(Cart.user_id == user_id)
    )
    cart = result.scalar_one_or_none()

    if not cart:
        return {"items": []}

    # Load cart items with variant and product
    result = await db.execute(
        select(CartItem)
        .options(
            selectinload(CartItem.variant)
            .selectinload(ProductVariant.product)
        )
        .where(CartItem.cart_id == cart.id)
    )
    items = result.scalars().all()

    items_response = []

    for i in items:
        variant = i.variant
        product = variant.product if variant else None

        # Fetch product price
        price = 0
        if product:
            result = await db.execute(
                select(Price).where(
                    Price.product_id == product.id
                )
            )
            price_obj = result.scalar_one_or_none()
            if price_obj:
                price = price_obj.amount

        items_response.append({
            "item_id": i.id,
            "variant_id": i.variant_id,
            "quantity": i.quantity,
            "price": price,
            "product": {
                "id": product.id if product else None,
                "name": product.name if product else "Product"
            }
        })
    return {
        "cart_id": cart.id,
        "items": items_response
    }
