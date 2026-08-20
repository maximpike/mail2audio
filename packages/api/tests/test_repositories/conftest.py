"""
Repository layer fixtures.

The `test_engine` / `test_db` fixtures live in the root conftest.py so the
model, schema and repository suites all share one definition.
"""

from datetime import datetime

import pytest


@pytest.fixture
def sample_email_data() -> dict:
    """Field values for a single email, matching the parser's output shape."""
    return {
        "subject": "Daily Market Update",
        "sender": "newsletter@vesact.com",
        "recipient": "user@example.com",
        "body_html": "<html><body><p>Market insights and analysis...</p></body></html>",
        "body_text": "Market insights and analysis...",
        "received_at": datetime(2025, 1, 15, 10, 30, 0),
    }


@pytest.fixture
def sample_emails() -> list[dict]:
    """Field values for several emails, for list and ordering assertions."""
    return [
        {
            "subject": "I like tacos",
            "sender": "support@vestact.com",
            "recipient": "user@example.com",
            "body_text": ("I'm quite partial to investing in large, founder-led businesses"),
            "received_at": datetime(2025, 7, 6, 6, 57, 53),
        },
        {
            "subject": "Clear vision",
            "sender": "support@vestact.com",
            "recipient": "user@example.com",
            "body_text": (
                "I was surprised to learn that there are now more listed ETFs "
                "than there are listed shares of companies in the US."
            ),
            "received_at": datetime(2025, 9, 21, 7, 40, 16),
        },
        {
            "subject": "Green and gold",
            "sender": "support@vestact.com",
            "recipient": "user@example.com",
            "body_text": (
                "US markets opened weaker on Friday, extending Thursday's "
                "sell-off, but staged a solid intraday rebound"
            ),
            "received_at": datetime(2025, 11, 17, 8, 26, 9),
        },
    ]
