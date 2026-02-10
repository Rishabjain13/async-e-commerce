from sqlalchemy import Column, Integer, String, Float
from app.database.base import Base

class ShippingMethod(Base):
    __tablename__ = "shipping_methods"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    cost = Column(Float)
    estimated_days = Column(Integer)
