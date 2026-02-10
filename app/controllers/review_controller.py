from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.models.review import Review

async def fetch_reviews(product_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Review).where(Review.product_id == product_id)
        )
        return result.scalar_one_or_none()
