from fastapi import APIRouter, Depends, HTTPException
from app.database.session import get_db
from app.schemas.cart import CartItemCreate, CartItemUpdate
from app.controllers.cart_controller import (
    add_item_to_cart,
    update_cart_item,
    remove_cart_item,
    get_cart
)

router = APIRouter(prefix="/cart", tags=["Cart"])

# For now: user_id passed manually (later replaced by JWT)
USER_ID = 1


@router.get("/")
async def fetch_cart(db=Depends(get_db)):
    return await get_cart(db, USER_ID)


@router.post("/items")
async def add_item(payload: CartItemCreate, db=Depends(get_db)):
    return await add_item_to_cart(
        db,
        USER_ID,
        payload.variant_id,
        payload.quantity
    )


@router.put("/items/{item_id}")
async def update_item(item_id: int, payload: CartItemUpdate, db=Depends(get_db)):
    item = await update_cart_item(db, item_id, payload.quantity)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/items/{item_id}")
async def delete_item(item_id: int, db=Depends(get_db)):
    result = await remove_cart_item(db, item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result
