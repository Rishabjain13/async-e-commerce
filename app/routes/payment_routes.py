from fastapi import APIRouter, Depends, HTTPException
from app.database.session import get_db
from app.schemas.payment import PaymentInitiate, PaymentWebhook
from app.controllers.payment_controller import (
    initiate_payment,
    payment_webhook,
    get_payment
)

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/initiate")
async def initiate(payload: PaymentInitiate, db=Depends(get_db)):
    payment = await initiate_payment(
        db,
        payload.order_id,
        payload.provider
    )
    if not payment:
        raise HTTPException(status_code=404, detail="Order not found")
    return payment


@router.post("/webhook")
async def webhook(payload: PaymentWebhook, db=Depends(get_db)):
    payment = await payment_webhook(
        db,
        payload.order_id,
        payload.status
    )
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("/{order_id}")
async def get(order_id: int, db=Depends(get_db)):
    payment = await get_payment(db, order_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
