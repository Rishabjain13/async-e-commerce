from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from app.database.base import Base
from sqlalchemy.orm import relationship

class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    sku = Column(String(50), unique=True, nullable=False)

    attributes = Column(JSON, nullable=False)  
    # example: {"size": "M", "color": "Black"}
    product = relationship("Product")
