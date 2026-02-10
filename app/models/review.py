from sqlalchemy import Column, Integer, ForeignKey, Numeric
from app.database.base import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    rating = Column(Numeric(3, 2), nullable=True)
