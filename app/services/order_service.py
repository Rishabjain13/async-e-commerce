import asyncio
from sqlalchemy.future import select
from app.database.session import AsyncSessionLocal

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.product_variant import ProductVariant
from app.models.product import Product


async def get_order_details(db, order_id: int):
    """
    Fetch order, items, and payment concurrently
    using separate DB sessions.
    """

    async def fetch_order():
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Order).where(Order.id == order_id)
            )
            return result.scalar_one_or_none()

    async def fetch_items():
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(OrderItem).where(OrderItem.order_id == order_id)
            )
            return result.scalars().all()

    async def fetch_payment():
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Payment).where(Payment.order_id == order_id)
            )
            return result.scalar_one_or_none()

    # ✅ Now safe to gather
    order, items, payment = await asyncio.gather(
        fetch_order(),
        fetch_items(),
        fetch_payment()
    )

    if not order:
        return None

    response_items = []
    total_amount = 0

    for item in items:
        async with AsyncSessionLocal() as session:
            variant = await session.get(ProductVariant, item.variant_id)
            product = None

            if variant:
                product = await session.get(Product, variant.product_id)

        price = float(item.price or 0)
        total_amount += price * item.quantity

        response_items.append({
            "item_id": item.id,
            "product_name": product.name if product else "Unknown",
            "quantity": item.quantity,
            "price": price
        })

    return {
        "order_id": order.id,
        "status": order.status,
        "items": response_items,
        "total_amount": total_amount,
        "payment": {
            "status": payment.status if payment else "pending"
        }
    }
