"""
Tests for the Email ORM model.

These pin down what the parser is actually allowed to produce. Real newsletters
are messy: some carry no HTML part at all, and some have Date headers that
cannot be parsed. The model has to survive both without inventing data.
"""

from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from app.models import AudioClip, AudioClipStatus, Email


def _minimal_email(**overrides) -> Email:
    """An Email with only the fields the parser always manages to fill."""
    fields = {
        "subject": "Daily Market Update",
        "sender": "newsletter@vestact.com",
        "recipient": "user@example.com",
    }
    fields.update(overrides)
    return Email(**fields)


class TestEmailPersistence:
    """The columns the parser cannot always populate must be nullable."""

    def test_persists_with_only_the_always_present_fields(self, test_db: Session):
        """Subject, sender and recipient alone are enough to store an email."""
        # Arrange
        email = _minimal_email()

        # Act
        test_db.add(email)
        test_db.commit()

        # Assert
        assert email.id is not None
        assert email.subject == "Daily Market Update"

    def test_body_html_may_be_none(self, test_db: Session):
        """A plain-text-only newsletter has no HTML part to store."""
        # Arrange
        email = _minimal_email(body_html=None, body_text="Plain text only")

        # Act
        test_db.add(email)
        test_db.commit()

        # Assert
        assert email.id is not None
        assert email.body_html is None
        assert email.body_text == "Plain text only"

    def test_body_text_may_be_none(self, test_db: Session):
        """Extraction can yield nothing while the raw HTML is still worth keeping."""
        # Arrange
        email = _minimal_email(body_html="<html></html>", body_text=None)

        # Act
        test_db.add(email)
        test_db.commit()

        # Assert
        assert email.id is not None
        assert email.body_text is None

    def test_received_at_may_be_none(self, test_db: Session):
        """An unparseable Date header must not block ingestion."""
        # Arrange
        email = _minimal_email(received_at=None)

        # Act
        test_db.add(email)
        test_db.commit()

        # Assert
        assert email.id is not None
        assert email.received_at is None

    def test_user_id_is_optional(self, test_db: Session):
        """Uploads are unauthenticated until the auth story lands."""
        # Arrange
        email = _minimal_email()

        # Act
        test_db.add(email)
        test_db.commit()

        # Assert
        assert email.user_id is None


class TestEmailTimestamps:
    """created_at/updated_at come from the database, not the caller."""

    def test_created_at_is_set_automatically(self, test_db: Session):
        """The parser never supplies created_at, so the column must default it."""
        # Arrange
        email = _minimal_email()

        # Act
        test_db.add(email)
        test_db.commit()

        # Assert
        assert isinstance(email.created_at, datetime)

    def test_updated_at_is_set_automatically(self, test_db: Session):
        """updated_at is populated on insert, not left null until first edit."""
        # Arrange
        email = _minimal_email()

        # Act
        test_db.add(email)
        test_db.commit()

        # Assert
        assert isinstance(email.updated_at, datetime)


class TestEmailAudioRelationship:
    """has_audio and audio_path are derived from clips, never stored."""

    def test_has_no_audio_when_there_are_no_clips(self, test_db: Session):
        """A freshly ingested email has nothing to play."""
        # Arrange
        email = _minimal_email()

        # Act
        test_db.add(email)
        test_db.commit()

        # Assert
        assert email.audio_clips == []
        assert email.has_audio is False
        assert email.audio_path is None

    def test_pending_clip_does_not_count_as_audio(self, test_db: Session):
        """Generation that has not finished must not advertise a playable file."""
        # Arrange
        email = _minimal_email()
        email.audio_clips.append(AudioClip(status=AudioClipStatus.PENDING))

        # Act
        test_db.add(email)
        test_db.commit()

        # Assert
        assert email.has_audio is False
        assert email.audio_path is None

    def test_ready_clip_exposes_its_path(self, test_db: Session):
        """Once a clip is ready, the email surfaces its storage path."""
        # Arrange
        email = _minimal_email()
        email.audio_clips.append(
            AudioClip(status=AudioClipStatus.READY, storage_path="media/1.mp3")
        )

        # Act
        test_db.add(email)
        test_db.commit()

        # Assert
        assert email.has_audio is True
        assert email.audio_path == "media/1.mp3"

    def test_deleting_email_removes_its_clips(self, test_db: Session):
        """Clips have no meaning without their email."""
        # Arrange
        email = _minimal_email()
        email.audio_clips.append(AudioClip(status=AudioClipStatus.READY))
        test_db.add(email)
        test_db.commit()
        assert test_db.query(AudioClip).count() == 1

        # Act
        test_db.delete(email)
        test_db.commit()

        # Assert
        assert test_db.query(AudioClip).count() == 0


class TestEmailRequiredFields:
    """The three fields the parser always falls back to must stay NOT NULL."""

    @pytest.mark.parametrize("field", ["subject", "sender", "recipient"])
    def test_required_field_rejects_none(self, test_db: Session, field: str):
        """The parser substitutes defaults for these, so null indicates a real bug."""
        # Arrange
        from sqlalchemy.exc import IntegrityError

        email = _minimal_email(**{field: None})

        # Act / Assert
        test_db.add(email)
        with pytest.raises(IntegrityError):
            test_db.commit()
