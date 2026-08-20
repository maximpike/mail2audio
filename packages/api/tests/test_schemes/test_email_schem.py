"""
Tests for the Email Pydantic schemas.

Two things are pinned here: that EmailCreate accepts exactly what the parser
produces, and that the length constraints are actually enforced. The original
schema wrote `minlength=` -- which Pydantic v2 silently ignores -- so the
validation everyone assumed was running never ran at all.
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.models import AudioClip, AudioClipStatus, Email
from app.schemas.email import EmailCreate, EmailResponse


@pytest.fixture
def parser_output() -> dict:
    """Exactly the shape EmailParser.parse_eml_file returns."""
    return {
        "subject": "Daily Market Update",
        "sender": "newsletter@vestact.com",
        "recipient": "user@example.com",
        "received_at": datetime(2025, 1, 15, 10, 30, 0),
        "body_html": "<html><body><p>Market insights</p></body></html>",
        "body_text": "Market insights",
    }


class TestEmailCreate:
    def test_accepts_parser_output_unchanged(self, parser_output: dict):
        """The parser's dict must drop straight into the schema."""
        # Act
        dto = EmailCreate(**parser_output)

        # Assert
        assert dto.subject == "Daily Market Update"
        assert dto.body_text == "Market insights"

    def test_accepts_missing_body_and_date(self):
        """A plain-text email with an unreadable Date header is still valid."""
        # Act
        dto = EmailCreate(
            subject="No body",
            sender="newsletter@vestact.com",
            recipient="user@example.com",
            received_at=None,
            body_html=None,
            body_text=None,
        )

        # Assert
        assert dto.received_at is None
        assert dto.body_html is None

    def test_rejects_empty_subject(self):
        """min_length must be enforced -- the old `minlength=` spelling was a no-op."""
        # Act / Assert
        with pytest.raises(ValidationError):
            EmailCreate(
                subject="",
                sender="newsletter@vestact.com",
                recipient="user@example.com",
            )

    def test_rejects_oversized_subject(self):
        """Subject is String(500) in the model; the schema must agree."""
        # Act / Assert
        with pytest.raises(ValidationError):
            EmailCreate(
                subject="x" * 501,
                sender="newsletter@vestact.com",
                recipient="user@example.com",
            )

    def test_rejects_missing_sender(self):
        """Sender is required -- the parser falls back to 'Unknown' rather than omitting it."""
        # Act / Assert
        with pytest.raises(ValidationError):
            EmailCreate(subject="Subject", recipient="user@example.com")


class TestEmailResponse:
    def test_reads_from_an_orm_instance(self, test_db):
        """from_attributes must be set, or model_validate on an ORM row fails."""
        # Arrange
        email = Email(
            subject="Daily Market Update",
            sender="newsletter@vestact.com",
            recipient="user@example.com",
            body_text="Market insights",
        )
        test_db.add(email)
        test_db.commit()

        # Act
        response = EmailResponse.model_validate(email)

        # Assert
        assert response.id == email.id
        assert response.subject == "Daily Market Update"
        assert isinstance(response.created_at, datetime)

    def test_reports_no_audio_for_a_fresh_email(self, test_db):
        """has_audio is derived, so a new email reports False rather than null."""
        # Arrange
        email = Email(
            subject="Subject",
            sender="newsletter@vestact.com",
            recipient="user@example.com",
        )
        test_db.add(email)
        test_db.commit()

        # Act
        response = EmailResponse.model_validate(email)

        # Assert
        assert response.has_audio is False
        assert response.audio_path is None

    def test_surfaces_a_ready_clip(self, test_db):
        """A ready clip must reach the API response as has_audio/audio_path."""
        # Arrange
        email = Email(
            subject="Subject",
            sender="newsletter@vestact.com",
            recipient="user@example.com",
        )
        email.audio_clips.append(
            AudioClip(status=AudioClipStatus.READY, storage_path="media/1.mp3")
        )
        test_db.add(email)
        test_db.commit()

        # Act
        response = EmailResponse.model_validate(email)

        # Assert
        assert response.has_audio is True
        assert response.audio_path == "media/1.mp3"
