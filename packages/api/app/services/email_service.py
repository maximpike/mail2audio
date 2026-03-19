"""
EmailService - Orchestrates email parsing and database persistence

This service layer sits between the API routes and the data layer, handling business logic for processing .eml files
"""
from typing import List, Optional
from fastapi.params import Depends

from app.models import Email
from app.repositories.email import EmailRepository
from app.schemas.email import EmailBase
from app.services.email_parser import EmailParser


#TODO Lots of work needed
class EmailService:
    """ Service for processing email files and managing email data
    Responsibilities:
    - Orchestrate email parsing via EmailParser
    - Persist emails to database via EmailRepository
    - Retrieve emails from database
    """

    def __init__(self, email_repo: EmailRepository = Depends()):
        self.email_repo = email_repo
        self.parser = EmailParser()

    def process_file(self, file_content: bytes) -> EmailBase:
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

        email_create = Email(**parsed_data)

        email_model = self.email_repo.create(email_create)

        return EmailBase.model_validate(email_model)

    # relates to create method in repo
    def create(self):
        # db_email = Email(**email_data.model_dump())
        pass

    # TODO: Evaluate return of get_all_emails
    def get_all_emails(self) -> List[EmailBase]:
        """ Retrieve all emails from database
        :returns List[EmailSchema] List of all emails
        """
        email_models = self.email_repo.get_all()

        # Need to ensure return ORM model I think its returning a Pydantic model atm
        result = []
        for email_model in email_models:
            email_schema = EmailBase.model_validate(email_model)
            result.append(email_schema)

        # Equivalent using List comprehension
        # return [EmailSchema.model_validate(email) for email in email_models]

        return result

    def get_by_id(self, email_id:int) -> Optional[EmailBase]:
        """ Retrieve a specific email by ID
        args: email_id -> The database id of the email
        :returns EmailSchema """
        email_model = self.email_repo.get_by_id(email_id)
        if email_model is None:
            return None
        return EmailBase.model_validate(email_model)

