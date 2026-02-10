from fastapi import APIRouter, Depends
from app.database.session import get_db
from app.controllers.shipping_controller import get_shipping_methods

router = APIRouter(prefix="/shipping", tags=["Shipping"])


@router.get("/methods")
async def list_shipping_methods(db=Depends(get_db)):
    return await get_shipping_methods(db)
