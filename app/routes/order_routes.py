from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.session import get_db
from app.controllers.order_controller import place_order
from app.services.order_service import get_order_details
from app.models.order import Order

router = APIRouter(prefix="/orders", tags=["Orders"])

USER_ID = 1

# GET all user orders

@router.get("/")
async def get_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Order).where(Order.user_id == USER_ID)
    )
    orders = result.scalars().all()

    return [
        {
            "id": o.id,
            "status": o.status,
            "total_amount": o.total_amount
        }
        for o in orders
    ]

# GET order details

@router.get("/{order_id}")
async def order_details(order_id: int, db: AsyncSession = Depends(get_db)):
    data = await get_order_details(db, order_id)
    if not data:
        raise HTTPException(status_code=404, detail="Order not found")
    return data

# CREATE order

@router.post("/")
async def create_order(db: AsyncSession = Depends(get_db)):
    order = await place_order(db, USER_ID)

    if not order:
        raise HTTPException(status_code=400, detail="Cart is empty")

    return {
        "order_id": order.id,
        "total_amount": order.total_amount,
        "status": order.status
    }
