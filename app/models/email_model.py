from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, UTC
from app.models.base import Base

class EmailModel(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(500), nullable=False)
    sender = Column(String(255))
    recipient = Column(String(255))
    received_at = Column(DateTime, nullable=False)
    body = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))