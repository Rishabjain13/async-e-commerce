import asyncio
from statistics import mean

from app.controllers.product_controller import fetch_product
from app.controllers.pricing_controller import fetch_price
from app.controllers.review_controller import fetch_reviews
from app.controllers.variant_read_controllers import (
    fetch_variants,
    fetch_inventory_map
)

async def safe_call(coro, timeout=2):
    try:
        return await asyncio.wait_for(coro, timeout)
    except Exception:
        return None


async def get_product_aggregate(product_id: int):
    product, price, reviews, variants = await asyncio.gather(
        safe_call(fetch_product(product_id)),
        safe_call(fetch_price(product_id)),
        safe_call(fetch_reviews(product_id)),
        safe_call(fetch_variants(product_id)),
    )

    if product is None or product.is_deleted:
        return None

    # Build variant inventory map
    variant_ids = [v.id for v in variants]
    inventory_map = await fetch_inventory_map(variant_ids)

    variant_response = []
    for v in variants:
        qty = inventory_map.get(v.id, 0)
        variant_response.append({
            "id": v.id,
            "sku": v.sku,
            "attributes": v.attributes,
            "quantity": qty,
            "in_stock": qty > 0
        })

        rating = 0.0

        if reviews:
            if isinstance(reviews, list) and len(reviews) > 0:
                ratings = [r.rating for r in reviews if hasattr(r, "rating")]
                if ratings:
                    rating = round(mean(ratings), 1)

            elif hasattr(reviews, "rating"):
                rating = float(reviews.rating)

    return {
        "product": {
            "id": product.id,
            "name": product.name,
            "description": product.description
        },
        "price": price.amount if price else None,
        "variants": variant_response,
        "rating": rating
    }
