from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    subject: Mapped[str] = mapped_column(String(500))
    sender: Mapped[str] = mapped_column(String(255))
    recipient: Mapped[str] = mapped_column(String(255))
    received_at: Mapped[datetime] = mapped_column(DateTime())  # Double check
    body: Mapped[str] = mapped_column(String())  # Check for TEXT Property
    created_at: Mapped[datetime] = mapped_column(DateTime())  # Double check

    # id = Column(Integer, primary_key=True, index=True)
    # subject = Column(String(500), nullable=False)
    # sender = Column(String(255))
    # recipient = Column(String(255))
    # received_at = Column(DateTime, nullable=False)
    # body = Column(Text)
    # created_at = Column(DateTime, default=lambda: datetime.now(UTC))
