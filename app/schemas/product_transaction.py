from pydantic import BaseModel
from typing import List, Dict, Optional

class VariantSchema(BaseModel):
    id: int
    sku: str
    attributes: dict
    quantity: int
    in_stock: bool

class ProductTransactionSchema(BaseModel):
    name: str
    description: str | None = None
    price: float
    variants: list[VariantSchema]
    rating: float | None = None