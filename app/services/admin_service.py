import asyncio
from sqlalchemy import func, select

from app.database.session import AsyncSessionLocal
from app.models.order import Order
from app.models.product import Product
from app.models.user import User

async def total_orders():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(func.count()).select_from(Order)
        )
        return result.scalar()


async def total_revenue():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(func.sum(Order.total_amount))
        )
        return result.scalar() or 0


async def total_products():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(func.count()).select_from(Product)
            .where(Product.is_deleted == False)
        )
        return result.scalar()


async def get_admin_stats():
    """
    Fetch admin dashboard metrics concurrently.
    Each task uses its own DB session.
    """

    orders, revenue, products = await asyncio.gather(
        total_orders(),
        total_revenue(),
        total_products()
    )

    return {
        "orders": orders,
        "revenue": float(revenue),
        "products": products
    }
