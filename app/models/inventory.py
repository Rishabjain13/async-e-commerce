from sqlalchemy import Column, Integer, ForeignKey
from app.database.base import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    variant_id = Column(Integer, ForeignKey("product_variants.id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False, default=0)
