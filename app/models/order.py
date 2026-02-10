from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime, timezone
from app.database.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    status = Column(String(20), default="PLACED")
    payment_status = Column(String(20), default="PENDING")

    total_amount = Column(Float, nullable=False)

    shipping_address_id = Column(Integer, ForeignKey("addresses.id"))
    shipping_method_id = Column(Integer, ForeignKey("shipping_methods.id"))
    shipping_cost = Column(Float, default=0)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
