from fastapi import APIRouter, Depends, HTTPException
from app.database.session import get_db
from app.schemas.product_transaction import ProductTransactionSchema
from app.controllers.product_transaction_controller import (
    create_full_product,
    update_full_product
)
from app.controllers.product_delete_controller import soft_delete_product
from app.deps import get_admin_user
from app.services.admin_service import get_admin_stats


router = APIRouter(prefix="/admin/products", tags=["Admin Products"])

@router.get("/stats")
async def admin_stats():
    return await get_admin_stats()

@router.post("")
async def create_product(
    payload: ProductTransactionSchema,
    db=Depends(get_db),
    _=Depends(get_admin_user)
):
    return await create_full_product(db, payload, performed_by="admin")


@router.put("/{product_id}")
async def update_product(
    product_id: int,
    payload: ProductTransactionSchema,
    db=Depends(get_db),
    _=Depends(get_admin_user)
):
    product = await update_full_product(db, product_id, payload, performed_by="admin")
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db=Depends(get_db),
    _=Depends(get_admin_user)
):
    product = await soft_delete_product(db, product_id, performed_by="admin")
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
