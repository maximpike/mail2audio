"""
Root conftest.py - Shared fixtures for entire test suite
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def test_app():
    """FastAPI application instance for testing"""
    return app


@pytest.fixture
def client(test_app):
    """FastAPI test client for E2E router tests"""
    return TestClient(test_app)


@pytest.fixture
def sample_email_html():
    """Reusable test email HTML for parser tests"""
    return """
    <html>
        <body>
            <h1>Investment Newsletter</h1>
            <p>Market insights here...</p>
            <footer>Unsubscribe | Privacy Policy</footer>
        </body>
    </html>
    """


@pytest.fixture
def sample_clean_text():
    """Expected output from parser for comparison"""
    return "Investment Newsletter\n\nMarket insights here..."
