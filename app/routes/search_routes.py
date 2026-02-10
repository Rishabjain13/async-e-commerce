from fastapi import APIRouter, Depends
from app.database.session import get_db
from app.controllers.search_controller import search_products
from app.schemas.search import ProductSearchParams

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("/products")
async def search(
    name: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    in_stock: bool | None = None,
    size: str | None = None,
    color: str | None = None,
    page: int = 1,
    limit: int = 10,
    db=Depends(get_db),
):
    params = ProductSearchParams(
        name=name,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        size=size,
        color=color,
        page=page,
        limit=limit
    )
    return await search_products(db, params)
