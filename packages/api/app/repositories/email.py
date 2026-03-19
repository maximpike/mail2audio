from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models import Email
from app.db import get_db


class EmailRepository:

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    # Should be ingesting with ORM models at this point
    def create(self, email: Email) -> Email:
        """ Store email in database """
        self.db.add(email)
        self.db.commit()
        self.db.refresh(email)
        return email

    def get_all(self) -> List[Email]:
        """ Get all emails """
        return list(self.db.scalars(select(Email)).all())

    def get_by_id(self, email_id: int) -> Optional[Email]:
        """ Get email by ID """
        return self.db.scalars(select(Email).where(Email.id == email_id)).first()

    def delete(self, email: Email):
        self.db.delete(email)
        self.db.commit()