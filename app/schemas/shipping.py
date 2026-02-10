from pydantic import BaseModel

class ShippingMethodResponse(BaseModel):
    id: int
    name: str
    cost: float
    estimated_days: int
