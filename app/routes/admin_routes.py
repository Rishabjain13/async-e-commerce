from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database.session import get_db
from app.models.order import Order
from app.models.product import Product
from app.models.price import Price
from app.deps import get_admin_user

router = APIRouter(prefix="/admin", tags=["Admin"],
                   dependencies=[Depends(get_admin_user)])


@router.get("/orders")
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order))
    orders = result.scalars().all()

    return [
        {
            "id": o.id,
            "user_id": o.user_id,
            "status": o.status
        }
        for o in orders
    ]

@router.get("/stats")
async def get_admin_stats(
    db: AsyncSession = Depends(get_db),
    admin = Depends(get_admin_user)):

    # Count only active products
    product_result = await db.execute(
        select(func.count(Product.id)).where(Product.is_deleted == False)
    )
    total_products = product_result.scalar() or 0
    
    # Count orders
    order_result = await db.execute(
        select(func.count(Order.id))
    )
    total_orders = order_result.scalar() or 0

    # Sum revenue
    revenue_result = await db.execute(
        select(func.sum(Order.total_amount))
    )
    total_revenue = revenue_result.scalar() or 0

    return {
        "total_products": int(total_products),
        "total_orders": int(total_orders),
        "total_revenue": float(total_revenue)
    }

@router.put("/orders/{order_id}")
async def update_order_status(order_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = data.get("status", order.status)
    await db.commit()

    return {"message": "Status updated"}

@router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()

    return {"message": "Product deleted"}


@router.put("/products/{product_id}")
async def update_product(product_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update product name
    if "name" in data:
        product.name = data["name"]

    # Update price
    if "price" in data:
        result = await db.execute(
            select(Price).where(Price.product_id == product_id)
        )
        price_obj = result.scalar_one_or_none()

        if price_obj:
            price_obj.amount = float(data["price"])

    await db.commit()

    return {"message": "Product updated"}
