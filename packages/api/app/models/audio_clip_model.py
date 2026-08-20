import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.email_model import Email


class AudioClipStatus(enum.StrEnum):
    """Lifecycle of a single text-to-speech render."""

    PENDING = "pending"
    GENERATING = "generating"
    READY = "ready"
    FAILED = "failed"


class AudioClip(Base, TimestampMixin):
    """A text-to-speech rendering of an email.

    Modelled as its own row rather than columns on Email because generation is
    fallible and not instantaneous: the UI needs to distinguish "not started"
    from "in progress" from "failed", and re-rendering in a different voice
    should add a clip rather than overwrite one.
    """

    __tablename__ = "audio_clips"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email_id: Mapped[int] = mapped_column(ForeignKey("emails.id", ondelete="CASCADE"), index=True)

    status: Mapped[AudioClipStatus] = mapped_column(
        Enum(AudioClipStatus, native_enum=False, length=16),
        default=AudioClipStatus.PENDING,
        nullable=False,
    )

    voice_id: Mapped[str | None] = mapped_column(String(64), default=None)

    # A local path today; an S3 object key once #16 lands. Kept deliberately
    # opaque so the storage backend can change without a migration.
    storage_path: Mapped[str | None] = mapped_column(String(1024), default=None)

    duration_seconds: Mapped[float | None] = mapped_column(Float(), default=None)

    # Populated on FAILED so a failure is inspectable without trawling logs.
    error_message: Mapped[str | None] = mapped_column(Text(), default=None)

    email: Mapped["Email"] = relationship(back_populates="audio_clips")
