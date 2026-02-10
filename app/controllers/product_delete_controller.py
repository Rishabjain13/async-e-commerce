from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.models.audit_log import AuditLog


async def soft_delete_product(
    db: AsyncSession,
    product_id: int,
    performed_by: str
):
    product = await db.get(Product, product_id)

    if not product or product.is_deleted:
        return None

    product.is_deleted = True
    product.deleted_at = datetime.utcnow()

    db.add(
        AuditLog(
            entity="Product",
            entity_id=product_id,
            action="DELETE",
            performed_by=performed_by
        )
    )

    await db.commit()
    return product
