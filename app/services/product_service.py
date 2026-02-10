import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.services.ecommerce_service import get_product_aggregate


async def get_all_products(db: AsyncSession):
    """
    Fetch all products and aggregate their data concurrently.
    """

    result = await db.execute(select(Product))
    products = result.scalars().all()

    # Create concurrent tasks
    tasks = [
        get_product_aggregate(product.id)
        for product in products
    ]

    aggregated = await asyncio.gather(*tasks)

    # Remove None results
    return [p for p in aggregated if p]
