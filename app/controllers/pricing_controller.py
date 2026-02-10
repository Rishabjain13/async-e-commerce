from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import AsyncSessionLocal
from app.models.price import Price

async def fetch_price(product_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Price).where(Price.product_id == product_id)
        )
        return result.scalar_one_or_none()
