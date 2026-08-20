"""
Tests for the AudioClip ORM model.

Audio generation is fallible and not instantaneous, so a clip is a row with a
lifecycle rather than a path column on Email. These tests pin that lifecycle.
"""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import AudioClip, AudioClipStatus, Email


@pytest.fixture
def stored_email(test_db: Session) -> Email:
    """A persisted Email to hang clips from."""
    email = Email(
        subject="Daily Market Update",
        sender="newsletter@vestact.com",
        recipient="user@example.com",
    )
    test_db.add(email)
    test_db.commit()
    return email


class TestAudioClipLifecycle:
    def test_defaults_to_pending(self, test_db: Session, stored_email: Email):
        """A clip exists before its audio does, so it starts pending."""
        # Arrange
        clip = AudioClip(email_id=stored_email.id)

        # Act
        test_db.add(clip)
        test_db.commit()

        # Assert
        assert clip.status == AudioClipStatus.PENDING
        assert clip.storage_path is None
        assert clip.duration_seconds is None

    def test_records_why_generation_failed(self, test_db: Session, stored_email: Email):
        """A failure needs to be inspectable without digging through logs."""
        # Arrange
        clip = AudioClip(
            email_id=stored_email.id,
            status=AudioClipStatus.FAILED,
            error_message="Polly rejected the text: too long",
        )

        # Act
        test_db.add(clip)
        test_db.commit()

        # Assert
        assert clip.status == AudioClipStatus.FAILED
        assert "too long" in clip.error_message

    def test_ready_clip_carries_path_voice_and_duration(
        self, test_db: Session, stored_email: Email
    ):
        """A finished clip holds everything the player needs."""
        # Arrange
        clip = AudioClip(
            email_id=stored_email.id,
            status=AudioClipStatus.READY,
            voice_id="Amy",
            storage_path="media/daily-update.mp3",
            duration_seconds=182.5,
        )

        # Act
        test_db.add(clip)
        test_db.commit()

        # Assert
        assert clip.voice_id == "Amy"
        assert clip.storage_path == "media/daily-update.mp3"
        assert clip.duration_seconds == pytest.approx(182.5)

    def test_one_email_can_have_several_clips(self, test_db: Session, stored_email: Email):
        """Re-generating in a different voice adds a clip, it does not overwrite."""
        # Arrange
        test_db.add_all(
            [
                AudioClip(email_id=stored_email.id, voice_id="Amy"),
                AudioClip(email_id=stored_email.id, voice_id="Brian"),
            ]
        )

        # Act
        test_db.commit()
        test_db.refresh(stored_email)

        # Assert
        assert len(stored_email.audio_clips) == 2
        assert {c.voice_id for c in stored_email.audio_clips} == {"Amy", "Brian"}


class TestAudioClipIntegrity:
    def test_requires_an_email(self, test_db: Session):
        """A clip cannot exist without the email it was generated from."""
        # Arrange
        clip = AudioClip(email_id=None)

        # Act / Assert
        test_db.add(clip)
        with pytest.raises(IntegrityError):
            test_db.commit()

    def test_rejects_an_email_id_that_does_not_exist(self, test_db: Session):
        """The FK must be enforced, not merely declared."""
        # Arrange
        clip = AudioClip(email_id=999999)

        # Act / Assert
        test_db.add(clip)
        with pytest.raises(IntegrityError):
            test_db.commit()

    def test_links_back_to_its_email(self, test_db: Session, stored_email: Email):
        """The relationship is navigable from the clip side too."""
        # Arrange
        clip = AudioClip(email_id=stored_email.id)

        # Act
        test_db.add(clip)
        test_db.commit()

        # Assert
        assert clip.email.id == stored_email.id
        assert clip.email.subject == "Daily Market Update"
