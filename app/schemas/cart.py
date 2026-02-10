from pydantic import BaseModel

class CartItemCreate(BaseModel):
    variant_id: int
    quantity: int


class CartItemUpdate(BaseModel):
    quantity: int
