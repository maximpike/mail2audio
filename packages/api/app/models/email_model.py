from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.audio_clip_model import AudioClip


class Email(Base, TimestampMixin):
    """An ingested email newsletter.

    Nullability here mirrors what EmailParser can actually guarantee. Subject,
    sender and recipient always get a value because the parser substitutes a
    fallback; everything else is genuinely optional, because real newsletters
    turn up with no HTML part or an unreadable Date header.
    """

    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Nullable until authentication lands -- uploads are currently anonymous.
    # Deliberately a plain column for now: the users table does not exist yet,
    # and declaring the FK before it does would break create_all and any insert
    # made with PRAGMA foreign_keys=ON. D3 adds users and promotes this to a
    # real ForeignKey in the same migration.
    user_id: Mapped[int | None] = mapped_column(index=True, default=None)

    subject: Mapped[str] = mapped_column(String(500))
    sender: Mapped[str] = mapped_column(String(255), index=True)
    recipient: Mapped[str] = mapped_column(String(255))

    # The Date header is frequently missing or malformed; refusing the email
    # over it would lose more than it protects.
    received_at: Mapped[datetime | None] = mapped_column(default=None)

    # Both representations are kept: the raw HTML so text extraction can be
    # re-run after the extractor improves, the text so the TTS stage and the
    # UI do not have to parse HTML themselves.
    body_html: Mapped[str | None] = mapped_column(Text(), default=None)
    body_text: Mapped[str | None] = mapped_column(Text(), default=None)

    audio_clips: Mapped[list["AudioClip"]] = relationship(
        back_populates="email",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def has_audio(self) -> bool:
        """Whether a playable clip exists, as opposed to one still being made."""
        from app.models.audio_clip_model import AudioClipStatus

        return any(clip.status is AudioClipStatus.READY for clip in self.audio_clips)

    @property
    def audio_path(self) -> str | None:
        """Storage path of the most recent ready clip, if there is one."""
        from app.models.audio_clip_model import AudioClipStatus

        ready = [c for c in self.audio_clips if c.status is AudioClipStatus.READY]
        if not ready:
            return None
        return max(ready, key=lambda c: c.id or 0).storage_path
