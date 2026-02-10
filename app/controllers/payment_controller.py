import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.payment import Payment
from app.models.order import Order


async def initiate_payment(db: AsyncSession, order_id: int, provider: str):
    async with db.begin():
        order = await db.get(Order, order_id)
        if not order:
            return None

        payment = Payment(
            order_id=order_id,
            provider=provider,
            amount=order.total_amount,
            status="INITIATED"
        )
        db.add(payment)

        order.payment_status = "PENDING"

    # simulate async gateway processing
    asyncio.create_task(simulate_gateway_webhook(order_id))

    return payment


async def simulate_gateway_webhook(order_id: int):
    """
    Simulates external payment gateway.
    """
    await asyncio.sleep(3)

    from app.database.session import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        async with db.begin():
            result = await db.execute(
                select(Payment).where(Payment.order_id == order_id)
            )
            payment = result.scalar_one_or_none()
            if not payment:
                return

            payment.status = "SUCCESS"

            order = await db.get(Order, order_id)
            order.payment_status = "SUCCESS"
            order.status = "CONFIRMED"


async def payment_webhook(db: AsyncSession, order_id: int, status: str):
    async with db.begin():
        result = await db.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        payment = result.scalar_one_or_none()
        if not payment:
            return None

        payment.status = status

        order = await db.get(Order, order_id)
        order.payment_status = status

        if status == "SUCCESS":
            order.status = "CONFIRMED"
        else:
            order.status = "PAYMENT_FAILED"

    return payment


async def get_payment(db: AsyncSession, order_id: int):
    result = await db.execute(
        select(Payment).where(Payment.order_id == order_id)
    )
    return result.scalar_one_or_none()
