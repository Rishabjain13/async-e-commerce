from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.session import AsyncSessionLocal
from app.models.product_variant import ProductVariant
from app.models.inventory import Inventory

async def fetch_variants(product_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ProductVariant).where(ProductVariant.product_id == product_id)
        )
        return result.scalars().all()

async def fetch_inventory_map(variant_ids: list[int]):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Inventory).where(Inventory.variant_id.in_(variant_ids))
        )
        return {inv.variant_id: inv.quantity for inv in result.scalars()}
