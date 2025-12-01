"""
EmailService - Orchestrates email parsing and database persistence

This service layer sits between the API routes and the data layer, handling business logic for processing .eml files
"""
from typing import Union, List, Optional

from sqlalchemy.orm import Session

from repositories.email_repository import EmailRepository
from schemas.email_schema import EmailSchema, EmailCreate
from services.email_parser import EmailParser


class EmailService:
    """ Service for processing email files and managing email data
    Responsibilities:
    - Orchestrate email parsing via EmailParser
    - Persist emails to database via EmailRepository
    - Retrieve emails from database
    """

    def __init__(self, db: Session):
        """ Initialise service with database session
        args: db - SQLAlchemy session for database operations
        """
        self.db = db
        self.repository = EmailRepository(db)
        self.parser = EmailParser()

    def process_file(self, file_content: bytes) -> EmailSchema:
        """ Process an uploaded .eml file and save to database
        args: file_content - Raw .eml file content as bytes (from file upoad)
        :returns EmailSchema - The created email with database ID
        :raises ValueError - If file_content is empty, None or invalid format
                TypeError -
        """
        if file_content is None:
            raise ValueError("File content cannot be None")

        if not isinstance(file_content, bytes):
            raise TypeError(f"Expected bytes or str, got {type(file_content)}")

        if len(file_content) == 0:
            raise ValueError("File content cannot be empty")

        try:
            parsed_data = self.parser.parse_eml_file(file_content) # do we decode in the service method or should we rather do this in the parser?
        except Exception as e:
            raise ValueError(f"Failed to parse email: {str(e)}") from e

        # Required fields?? otherwise no validation required
        if not parsed_data.get('subject'):
            raise ValueError("Invalid email format: missing subject")
        if not parsed_data.get('sender'):
            raise ValueError("Invalid email format: missing sender")

        email_create = EmailCreate(**parsed_data)

        email_model = self.repository.create(email_create)

        return EmailSchema.model_validate(email_model)

    def get_all(self) -> List[EmailSchema]:
        """ Retrieve all emails from database
        :returns List[EmailSchema] List of all emails
        """
        email_models = self.repository.get_all()

        result = []
        for email_model in email_models:
            email_schema = EmailSchema.model_validate(email_model)
            result.append(email_schema)

        # Equivalent using List comprehension
        # return [EmailSchema.model_validate(email) for email in email_models]

        return result

    def get_by_id(self, email_id:int) -> Optional[EmailSchema]:
        """ Retrieve a specific email by ID
        args: email_id -> The database id of the email
        :returns EmailSchema """
        email_model = self.repository.get_by_id(email_id)
        if email_model is None:
            return None
        return EmailSchema.model_validate(email_model)

