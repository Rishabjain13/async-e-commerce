from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.session import AsyncSessionLocal
from app.models.product import Product


async def fetch_product(product_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product).where(
                Product.id == product_id,
                Product.is_deleted == False
            )
        )
        return result.scalar_one_or_none()
