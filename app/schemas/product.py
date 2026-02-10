from pydantic import BaseModel
from typing import Optional


class ProductSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class PriceSchema(BaseModel):
    id: int
    product_id: int
    amount: float

    class Config:
        from_attributes = True


class InventorySchema(BaseModel):
    id: int
    product_id: int
    in_stock: bool

    class Config:
        from_attributes = True


class ReviewSchema(BaseModel):
    id: int
    product_id: int
    rating: Optional[float] = None

    class Config:
        from_attributes = True


class ProductAggregateSchema(BaseModel):
    product: Optional[ProductSchema]
    price: Optional[PriceSchema]
    inventory: Optional[InventorySchema]
    review: Optional[ReviewSchema]
