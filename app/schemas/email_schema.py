from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class EmailBase(BaseModel):
    """ Base schema with field common to all email operations"""
    subject: str
    sender: str
    recipient: str
    body: Optional[str] = None

class EmailCreate(EmailBase):
    """ Schema for creating a new email (inout for API/IMAP) """
    received_at: Optional[datetime] = None
    pass


class EmailSchema(EmailBase):
    """ Schema for reading an email (output from API) """
    id: int
    received_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
