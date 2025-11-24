from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.email_model import EmailModel
from app.schemas.email_schema import EmailCreate


class EmailRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, email_data: EmailCreate) -> EmailModel:
        """ Store email in database """
        db_email = EmailModel(**email_data.model_dump())
        self.db.add(db_email)
        self.db.commit()
        self.db.refresh(db_email)
        return db_email

    def get_all(self) -> List[EmailModel]:
        """ Get all emails """
        return self.db.query(EmailModel).all() # type: ignore

    def get_by_id(self, email_id: int) -> Optional[EmailModel]:
        """ Get email by ID """
        return self.db.get(EmailModel, email_id)
