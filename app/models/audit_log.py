from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.database.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    entity = Column(String(50))
    entity_id = Column(Integer)
    action = Column(String(50))
    performed_by = Column(String(50))
    timestamp = Column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc)
)

