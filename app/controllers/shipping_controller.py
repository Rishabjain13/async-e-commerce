from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.shipping import ShippingMethod


async def get_shipping_methods(db: AsyncSession):
    result = await db.execute(select(ShippingMethod))
    return result.scalars().all()
