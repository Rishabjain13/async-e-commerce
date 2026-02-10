from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from app.models.product import Product
from app.models.price import Price
from app.models.product_variant import ProductVariant
from app.models.inventory import Inventory


async def search_products(db: AsyncSession, params):
    query = (
        select(Product, Price, ProductVariant, Inventory)
        .join(Price, Price.product_id == Product.id)
        .join(ProductVariant, ProductVariant.product_id == Product.id)
        .join(Inventory, Inventory.variant_id == ProductVariant.id)
        .where(Product.is_deleted == False)
    )

    filters = []

    if params.name:
        filters.append(Product.name.ilike(f"%{params.name}%"))

    if params.min_price is not None:
        filters.append(Price.amount >= params.min_price)

    if params.max_price is not None:
        filters.append(Price.amount <= params.max_price)

    if params.in_stock:
        filters.append(Inventory.quantity > 0)

    if params.size:
        filters.append(
            ProductVariant.attributes["size"].astext == params.size
        )

    if params.color:
        filters.append(
            ProductVariant.attributes["color"].astext == params.color
        )

    if filters:
        query = query.where(and_(*filters))

    # Pagination
    offset = (params.page - 1) * params.limit
    query = query.offset(offset).limit(params.limit)

    result = await db.execute(query)
    rows = result.all()

    products = {}
    for product, price, variant, inventory in rows:
        if product.id not in products:
            products[product.id] = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": price.amount,
                "variants": []
            }

        products[product.id]["variants"].append({
            "sku": variant.sku,
            "attributes": variant.attributes,
            "quantity": inventory.quantity,
            "in_stock": inventory.quantity > 0
        })

    return list(products.values())
