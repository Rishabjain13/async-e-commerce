from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.address import Address


async def create_address(db: AsyncSession, user_id: int, data):
    async with db.begin():
        address = Address(
            user_id=user_id,
            name=data.name,
            phone=data.phone,
            line1=data.line1,
            city=data.city,
            state=data.state,
            pincode=data.pincode,
            country=data.country,
            is_default=data.is_default
        )
        db.add(address)
        await db.flush()
        return address


async def get_user_addresses(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Address).where(Address.user_id == user_id)
    )
    return result.scalars().all()
