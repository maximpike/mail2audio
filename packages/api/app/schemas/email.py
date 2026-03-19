from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# TODO Shouldnt be labeled as an DTO input its just a BASE
class EmailBase(BaseModel):
    """ Input DTO Base schema with fields common to all email operations"""
    subject: str = Field(..., minlength=1, max_length=500)
    sender: str = Field(..., minlength=5, max_length=255)
    recipient: str = Field(..., minlength=5, max_length=255)
    body: Optional[str] = None

class EmailResponse(EmailBase):
    """ Output DTO Schema for reading an email """
    id: int
    received_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
