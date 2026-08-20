"""
Base class and shared mixins for all database models/entities.
"""

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class TimestampMixin:
    """Adds database-managed created_at/updated_at to a model.

    These are deliberately server-side defaults rather than Python ones: the
    parser never supplies them, and a caller that forgets to set created_at
    should still get a valid row rather than a NOT NULL violation.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=func.now(), onupdate=func.now(), nullable=False
    )
