from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.models.inventory import Inventory

async def fetch_inventory(product_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Inventory).where(Inventory.product_id == product_id)
        )
        return result.scalar_one_or_none()
