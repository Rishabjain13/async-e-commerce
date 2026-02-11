from pydantic import BaseModel
from typing import List, Dict, Optional

class VariantSchema(BaseModel):
    sku: str
    attributes: dict[str,str]
    quantity: int

class ProductTransactionSchema(BaseModel):
    name: str
    description: str | None = None
    price: float
    variants: list[VariantSchema]
    rating: float | None = None
