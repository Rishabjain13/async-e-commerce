from fastapi import APIRouter, HTTPException, Depends
from app.database.session import get_db
from app.services.ecommerce_service import get_product_aggregate
from app.services.product_service import get_all_products
from app.core.cache import get_cache, set_cache

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/{product_id}")
async def get_product(product_id: int):
    cache_key = f"product:{product_id}"

    cached = get_cache(cache_key)
    if cached:
        return {"source": "cache", "data": cached}

    data = await get_product_aggregate(product_id)

    if data is None:
        raise HTTPException(status_code=404, detail="Product not found")

    set_cache(cache_key, data)
    return data

@router.get("")
async def list_products(db=Depends(get_db)):
    return await get_all_products(db)
