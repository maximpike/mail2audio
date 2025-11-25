import email
from typing import Optional
from datetime import datetime
from email.utils import parsedate_to_datetime
from email.message import Message
from html.parser import HTMLParser


class EmailParser:
    """ Service for parsing .eml files and extracting clean text content """

    @staticmethod
    def parse_eml_file(eml_content: bytes) -> dict:
        """ Parse .eml file content and extract relevant fields.
        args: eml_content - raw bytes of .eml file
        :returns dict with keys: subject, sender, recipient, received_at, body
        """
        msg: Message = email.message_from_bytes(eml_content)

        html_content = EmailParser._get_html_content(msg)
        if html_content:
            body_text = EmailParser._html_to_text(html_content)
        else:
            body_text = None

        print("body_text:")
        print(body_text)

        return {
            "subject": (msg.get("Subject", "No Subject") or "No Subject").strip(),
            "sender": (msg.get("From", "Unknown") or "Unknown").strip(),
            "recipient": (msg.get("To", "Unknown") or "Unknown").strip(),
            "received_at": EmailParser._parse_date(msg.get("Date")),
            "body": body_text
        }

    @staticmethod
    def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
        """ Parse email date string to datetime object.
        args: date_str - RFC 2822 formatted date string from email header
        :returns datetime object or None if parsing fails
        """
        if not date_str:
            return None
        try:
            return parsedate_to_datetime(date_str)
        except Exception:
            return None

    @staticmethod
    def _get_message_object(eml_content: bytes):
        """ Convert raw .eml bytes to Message object.
        args: eml_content - Raw bytes of .eml file
        :returns Message object
        """
        return email.message_from_bytes(eml_content)

    @staticmethod
    def _get_html_content(msg: Message) -> Optional[str]:
        """
        Extract HTML content from email message.
        Handles both multipart and single-part messages
        args: msg - Email message argument
        :returns HTML content as string or None if no HTML found"""
        # Check if email has multiple parts (multipart email)
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == f"text/html":
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode('utf-8', errors='ignore')
        else:
            if msg.get_content_type() == f"text/html":
                payload = msg.get_payload(decode=True)
                if payload:
                    return payload.decode('utf-8', errors='ignore')
        return None

    @staticmethod
    def _html_to_text(html_content: str) -> str:
        """ Convert HTML to plain text using Python's built-in html.parser
        args: html_content - raw HTML string
        :returns Plain text extracted from HTML
        """
        parser = HTMLTextExtractor()
        parser.feed(html_content)
        return parser.get_text()

# TODO: Refactor into separate python file (encompass service layer)
class HTMLTextExtractor(HTMLParser):
    """
    Custom HTML parser that extracts text content from HTML.
    Uses Python's built-in html.parser for security and stability.
    """

    def __init__(self):
        super().__init__() # Inheritance
        self.text_parts = []
        self.skip_tags = {'script', 'style'}  # Tags to completely ignore
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        """Called when a start tag is encountered"""
        self.current_tag = tag

    def handle_endtag(self, tag):
        """Called when an end tag is encountered"""
        self.current_tag = None

    def handle_data(self, data):
        """Called when text data is encountered"""
        # Skip data inside script and style tags
        if self.current_tag not in self.skip_tags:
            # Strip whitespace and add if not empty
            text = data.strip()
            if text:
                self.text_parts.append(text)

    def get_text(self) -> str:
        """Return all extracted text joined with spaces"""
        return ' '.join(self.text_parts)
