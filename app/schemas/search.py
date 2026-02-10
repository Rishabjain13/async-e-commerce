from pydantic import BaseModel
from typing import Optional


class ProductSearchParams(BaseModel):
    name: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    in_stock: Optional[bool] = None
    size: Optional[str] = None
    color: Optional[str] = None
    page: int = 1
    limit: int = 10
