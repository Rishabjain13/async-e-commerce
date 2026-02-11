from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database.session import get_db
from app.models.order import Order
from app.models.product import Product
from app.models.price import Price
from app.models.review import Review
from app.models.product_variant import ProductVariant
from app.models.inventory import Inventory
from app.schemas.product_transaction import ProductTransactionSchema
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

@router.post("/products")
async def create_product(
    data: ProductTransactionSchema,
    db: AsyncSession = Depends(get_db)
):

    async with db.begin():

        # 1️⃣ Create Product
        product = Product(
            name=data.name,
            description=data.description,
            is_deleted=False
        )

        db.add(product)
        await db.flush()

        # 2️⃣ Create Price
        price = Price(
            product_id=product.id,
            amount=data.price
        )
        db.add(price)

        # 3️⃣ Create Variants
        for variant_data in data.variants:

            variant = ProductVariant(
                product_id=product.id,
                sku=variant_data.sku,
                attributes=variant_data.attributes
            )

            db.add(variant)
            await db.flush()

            inventory = Inventory(
                variant_id=variant.id,
                quantity=variant_data.quantity
            )

            db.add(inventory)

        # 4️⃣ CREATE REVIEW FOR RATING
        if hasattr(data, "rating") and data.rating is not None:

            review = Review(
                product_id=product.id,
                rating=data.rating
            )

            db.add(review)

    return {
        "message": "Product created successfully",
        "product_id": product.id
    }


@router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_deleted = True
    await db.commit()

    return {"message": "Product deleted"}

@router.put("/products/{product_id}")
async def update_product(
    product_id: int,
    data: ProductTransactionSchema,
    db: AsyncSession = Depends(get_db)
):

    async with db.begin():

        # 1️⃣ Fetch Product
        product = await db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        product.name = data.name
        product.description = data.description

        # 2️⃣ Update Price
        result = await db.execute(
            select(Price).where(Price.product_id == product_id)
        )
        price_obj = result.scalar_one_or_none()
        if price_obj:
            price_obj.amount = data.price

        # 3️⃣ Update Variant (Assuming single variant)
        result = await db.execute(
            select(ProductVariant).where(
                ProductVariant.product_id == product_id
            )
        )
        variant = result.scalar_one_or_none()

        if variant:
            variant.sku = data.variants[0].sku
            variant.attributes = data.variants[0].attributes

            # Update Inventory
            result = await db.execute(
                select(Inventory).where(
                    Inventory.variant_id == variant.id
                )
            )
            inventory = result.scalar_one_or_none()

            if inventory:
                inventory.quantity = data.variants[0].quantity

        # 4️⃣ Update Review (rating)
        from app.models.review import Review

        result = await db.execute(
            select(Review).where(Review.product_id == product_id)
        )
        review = result.scalar_one_or_none()

        if review:
            review.rating = data.rating
        else:
            review = Review(
                product_id=product_id,
                rating=data.rating
            )
            db.add(review)

    return {"message": "Product fully updated"}

