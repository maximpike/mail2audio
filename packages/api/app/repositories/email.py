from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Email


class EmailRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    # Should be ingesting with ORM models at this point
    def create(self, email: Email) -> Email:
        """Store email in database"""
        self.db.add(email)
        self.db.commit()
        self.db.refresh(email)
        return email

    def get_all(self) -> list[Email]:
        """Get all emails"""
        return list(self.db.scalars(select(Email)).all())

    def get_by_id(self, email_id: int) -> Email | None:
        """Get email by ID"""
        return self.db.scalars(select(Email).where(Email.id == email_id)).first()

    def delete(self, email: Email):
        self.db.delete(email)
        self.db.commit()
