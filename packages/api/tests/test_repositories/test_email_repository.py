"""
Tests for EmailRepository.

Rewritten to pass ORM entities rather than Pydantic DTOs. The repository is the
data-access layer, so it deals in models; converting a validated DTO into an
Email is the service's job (AGENT_PLAYBOOK.md section 3 -- schemas belong at API
boundaries, models are internal).

The previous version imported an `EmailCreate` schema that had never been
written, so this module could not be collected at all.
"""

from sqlalchemy.orm import Session

from app.models import Email
from app.repositories.email import EmailRepository


def test_save_email(test_db: Session, sample_email_data: dict):
    """Test that repository can create and persist an email"""
    # Arrange
    repo = EmailRepository(test_db)
    email = Email(**sample_email_data)

    # Act
    created = repo.create(email)

    # Assert
    assert created.id is not None
    assert created.subject == "Daily Market Update"
    assert created.sender == "newsletter@vesact.com"


def test_persists_both_body_representations(test_db: Session, sample_email_data: dict):
    """Raw HTML and extracted text must both survive the round trip."""
    # Arrange
    repo = EmailRepository(test_db)
    email = Email(**sample_email_data)

    # Act
    created = repo.create(email)

    # Assert
    assert created.body_html is not None
    assert "<html>" in created.body_html
    assert created.body_text == "Market insights and analysis..."


def test_save_email_without_body_or_date(test_db: Session):
    """A plain-text newsletter with an unreadable Date header still persists."""
    # Arrange
    repo = EmailRepository(test_db)
    email = Email(
        subject="No body",
        sender="support@vestact.com",
        recipient="user@example.com",
        body_html=None,
        body_text=None,
        received_at=None,
    )

    # Act
    created = repo.create(email)

    # Assert
    assert created.id is not None
    assert created.body_html is None
    assert created.received_at is None


def test_get_all_emails(test_db: Session, sample_emails: list[dict]):
    """Test that repository can retrieve all emails"""
    # Arrange
    repo = EmailRepository(test_db)
    for data in sample_emails:
        repo.create(Email(**data))

    # Act
    all_emails = repo.get_all()

    # Assert
    assert len(all_emails) == len(sample_emails)


def test_get_email_by_id(test_db: Session, sample_email_data: dict):
    """Test that repository can retrieve email by ID"""
    # Arrange
    repo = EmailRepository(test_db)
    created_email = repo.create(Email(**sample_email_data))

    # Act
    retrieved_email = repo.get_by_id(created_email.id)

    # Assert
    assert retrieved_email is not None
    assert retrieved_email.id == created_email.id
    assert retrieved_email.subject == created_email.subject
    assert retrieved_email.sender == created_email.sender


def test_returns_none_for_nonexistent_id(test_db: Session, sample_email_data: dict):
    """Test that repository returns None for ID that doesn't exist"""
    # Arrange
    repo = EmailRepository(test_db)
    repo.create(Email(**sample_email_data))

    # Act
    result = repo.get_by_id(100)

    # Assert
    assert result is None


def test_delete_removes_the_email(test_db: Session, sample_email_data: dict):
    """Test that a deleted email is no longer retrievable"""
    # Arrange
    repo = EmailRepository(test_db)
    created = repo.create(Email(**sample_email_data))
    email_id = created.id

    # Act
    repo.delete(created)

    # Assert
    assert repo.get_by_id(email_id) is None
