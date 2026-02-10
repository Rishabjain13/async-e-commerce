from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.product import Product
from app.models.price import Price
from app.models.review import Review
from app.models.audit_log import AuditLog
from app.models.product_variant import ProductVariant
from app.models.inventory import Inventory


async def create_full_product(
    db: AsyncSession,
    data,
    performed_by: str
):
    async with db.begin():
        product = Product(
            name=data.name,
            description=data.description
        )
        db.add(product)
        await db.flush()

        # Price
        db.add(Price(product_id=product.id, amount=data.price))

        # Variants + Inventory
        for variant in data.variants:
            pv = ProductVariant(
                product_id=product.id,
                sku=variant.sku,
                attributes=variant.attributes
            )
            db.add(pv)
            await db.flush()

            db.add(
                Inventory(
                    variant_id=pv.id,
                    quantity=variant.quantity
                )
            )

        # Review (optional)
        if data.rating is not None:
            db.add(Review(product_id=product.id, rating=data.rating))

        # Audit
        db.add(AuditLog(
            entity="Product",
            entity_id=product.id,
            action="CREATE",
            performed_by=performed_by
        ))

    return product


async def update_full_product(
    db: AsyncSession,
    product_id: int,
    data,
    performed_by: str
):
    async with db.begin():
        product = await db.get(Product, product_id)
        if not product or product.is_deleted:
            return None

        product.name = data.name
        product.description = data.description

        # Update price
        price = await db.execute(
            select(Price).where(Price.product_id == product_id)
        )
        price.scalar_one().amount = data.price

        # Remove old variants & inventory
        old_variants = await db.execute(
            select(ProductVariant).where(ProductVariant.product_id == product_id)
        )
        old_variants = old_variants.scalars().all()

        for ov in old_variants:
            await db.execute(
                select(Inventory).where(Inventory.variant_id == ov.id)
            )
            await db.delete(ov)

        # Add new variants
        for variant in data.variants:
            pv = ProductVariant(
                product_id=product_id,
                sku=variant.sku,
                attributes=variant.attributes
            )
            db.add(pv)
            await db.flush()

            db.add(
                Inventory(
                    variant_id=pv.id,
                    quantity=variant.quantity
                )
            )

        # Update review
        if data.rating is not None:
            review = await db.execute(
                select(Review).where(Review.product_id == product_id)
            )
            review = review.scalar_one_or_none()
            if review:
                review.rating = data.rating
            else:
                db.add(Review(product_id=product_id, rating=data.rating))

        # Audit
        db.add(AuditLog(
            entity="Product",
            entity_id=product_id,
            action="UPDATE",
            performed_by=performed_by
        ))

    return product
