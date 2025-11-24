from sqlalchemy.orm import Session
from app.repositories.email_repository import EmailRepository
from app.schemas.email_schema import EmailCreate


def test_save_email(test_db: Session, sample_email_data):
    """ Test that repository can create and persist an email """
    # Arrange
    repo = EmailRepository(test_db)
    email_create = EmailCreate(**sample_email_data)

    # Act
    email = repo.create(email_create)

    # Assert
    assert email.id is not None
    assert email.subject == "Daily Market Update"
    assert email.sender == "newsletter@vesact.com"

def test_get_all_emails(test_db: Session, sample_emails):
    """ Test that repository can retrieve all emails """
    # Arrange
    repo = EmailRepository(test_db)
    for email in sample_emails:
        email_create = EmailCreate(**email)
        repo.create(email_create)

    # Act
    all_emails = repo.get_all()

    # Assert
    assert len(all_emails) == len(sample_emails)


def test_get_email_by_id(test_db: Session, sample_email_data):
    """ Test that repository can retrieve email by ID """
    # Arrange
    repo = EmailRepository(test_db)
    email_create = EmailCreate(**sample_email_data)
    created_email = repo.create(email_create)

    # Act
    retrieved_email = repo.get_by_id(created_email.id)

    # Assert
    assert retrieved_email is not None
    assert retrieved_email.id == created_email.id
    assert retrieved_email.subject == created_email.subject
    assert retrieved_email.sender == created_email.sender

def test_returns_none_for_nonexistent_id(test_db: Session, sample_email_data):
    """ Test that repository returns None for ID that doesn't exist"""
    # Arrange
    repo = EmailRepository(test_db)
    email_create = EmailCreate(**sample_email_data)
    repo.create(email_create)

    # Act
    result = repo.get_by_id(100)

    # Assert
    assert result is None
