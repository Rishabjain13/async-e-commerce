from pydantic import BaseModel

class PaymentInitiate(BaseModel):
    order_id: int
    provider: str = "mock_gateway"


class PaymentWebhook(BaseModel):
    order_id: int
    status: str
