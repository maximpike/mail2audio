from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EmailBase(BaseModel):
    """Fields common to every email representation.

    Note `min_length`, not `minlength`: Pydantic v2 silently ignores unknown
    keyword arguments, so the original spelling meant none of these length
    constraints were ever enforced.
    """

    subject: str = Field(..., min_length=1, max_length=500)
    sender: str = Field(..., min_length=1, max_length=255)
    recipient: str = Field(..., min_length=1, max_length=255)


class EmailCreate(EmailBase):
    """Input DTO -- exactly the shape EmailParser.parse_eml_file returns.

    Everything the parser cannot guarantee is optional, so a plain-text
    newsletter or one with an unreadable Date header still validates.
    """

    received_at: datetime | None = None
    body_html: str | None = None
    body_text: str | None = None


class EmailResponse(EmailBase):
    """Output DTO for reading an email.

    `has_audio` and `audio_path` are derived on the Email model from its
    audio clips rather than stored, so they stay correct as clips are added,
    finish or fail. `from_attributes` lets them be read straight off the ORM
    instance alongside the real columns.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    received_at: datetime | None = None
    body_html: str | None = None
    body_text: str | None = None
    has_audio: bool = False
    audio_path: str | None = None
    created_at: datetime
    updated_at: datetime
