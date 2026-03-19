"""
Tests for the email parser service.
Tests the HTML to text conversion, cleaning, and formatting.
"""
import pytest
from datetime import datetime
from pathlib import Path
from app.services.email_parser import EmailParser


class TestEmailParser:
    """ Test suite for email parsing functionality. """

class TestParseEmlFile:
    """ Tests for parse_eml_file method """

    def test_parse_basic_headers_from_email(self, sample_eml_files):
        """ Test parsing basic headers (subject, sender, recipient, date) """
        # Arrange
        with open(sample_eml_files["tacos"], "rb") as f:
            eml_content = f.read()

        # Act
        headers = EmailParser.parse_eml_file(eml_content)

        # Assert
        assert headers["subject"]
        assert headers["sender"]
        assert headers["recipient"]
        assert headers["received_at"]
        assert isinstance(headers["received_at"], datetime)

    def test_parse_body_from_email(self, sample_eml_files):
        """ Test complete email parsing including body text extraction """
        # Arrange
        with open(sample_eml_files["vision"], "rb") as f:
            eml_content = f.read()

        # Act
        body = EmailParser.parse_eml_file(eml_content)

        # Assert
        assert body["body"] is not None
        assert len(body["body"]) > 100  # Should have substantial content
        assert "US markets kicked off a packed earnings week on a strong note" in body["body"]
        assert "Emma Dunkley" in body["body"] or "FT's asset management reporter" in body["body"]


class TestExtractHtmlContent:
    """ Tests for extracting HTML from email messages. """

    def test_get_html_from_email(self, sample_eml_files):
        """ Test that we can extract HTML content from the email """
        # Arrange
        with open(sample_eml_files["tacos"], "rb") as f:
            eml_content = f.read()

        msg = EmailParser._get_message_object(eml_content)

        # Act
        html_content = EmailParser._get_html_content(msg)

        assert html_content is not None
        assert len(html_content) > 0
        assert "<html" in html_content.lower()
        assert "I'm quite partial" in html_content


class TestConvertHtmlToText:
    """Tests for converting HTML to plain text"""

    def test_convert_simple_html_to_text(self):
        """Test converting simple HTML to text"""
        # Arrange
        html = "<html><body><p>Hello World</p></body></html>"

        # Act
        text = EmailParser._html_to_text(html)

        # Assert
        assert "Hello World" in text
        assert "<html>" not in text
        assert "<p>" not in text

    def test_convert_email_html(self, sample_eml_files):
        """Test converting actual email HTML to text"""
        # Arrange
        with open(sample_eml_files["tacos"], "rb") as f:
            eml_content = f.read()
        msg = EmailParser._get_message_object(eml_content)
        html_content = EmailParser._get_html_content(msg)

        # Act
        text = EmailParser._html_to_text(html_content)

        # Assert
        assert text is not None
        assert len(text) > 0
        assert "founder-led businesses" in text
        assert "<td" not in text
        assert "<div" not in text

class TestParseDateMethod:
    """ Tests for _parse_date method """

    def test_parse_valid_rfc2822_date(self):
        """ Test parsing a valid RFC 2822 date string """
        # Arrange
        date_str = "Wed, 9 Jul 2025 06:57:53 +0000"

        # Act
        result = EmailParser._parse_date(date_str)

        # Assert
        assert result is not None
        assert isinstance(result, datetime)
        assert result.year == 2025
        assert result.month == 7
        assert result.day == 9

    def test_parse_none_date_returns_none(self):
        """ Test that None input returns None """
        # Arrange
        date_str = None

        # Act
        result = EmailParser._parse_date(date_str)

        # Assert
        assert result is None

    def test_parse_empty_string_returns_none(self):
        """ Test that empty string returns None """
        # Arrange
        date_str = ""

        # Act
        result = EmailParser._parse_date(date_str)

        # Assert
        assert result is None

    def test_parse_invalid_date_returns_none(self):
        """ Test that invalid date string returns None """
        # Arrange
        date_str = "not a valid date"

        # Act
        result = EmailParser._parse_date(date_str)

        # Assert
        assert result is None
