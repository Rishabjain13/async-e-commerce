from pydantic import BaseModel

class AddressCreate(BaseModel):
    name: str
    phone: str
    line1: str
    city: str
    state: str
    pincode: str
    country: str
    is_default: bool = False
