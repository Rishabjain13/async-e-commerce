from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database.base import Base

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    amount = Column(Float, nullable=False)
