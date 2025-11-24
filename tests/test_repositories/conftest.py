"""
Repository layer fixtures - Test database setup
"""
from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.base import Base  # Your SQLAlchemy Base


@pytest.fixture(scope="function")
def test_engine():
    """
    Create an in-memory SQLite engine for each test.
    Scope='function' ensures clean state per test.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},  # Required for SQLite
        echo=False
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(test_engine) -> Session:
    """
    Provide a SQLAlchemy session for repository tests.
    Automatically rolls back after each test.
    """
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def sample_email_data():
    """
    Sample email data for creating test records
    :return dict containing email data
    """
    return {
        "subject": "Daily Market Update",
        "sender": "newsletter@vesact.com",
        "recipient": "user@example.com",
        "body": "Market insights and analysis...",
        "received_at": datetime(2025, 1, 15, 10, 30, 0),
    }

@pytest.fixture
def sample_emails():
    """ Sample list of emails and their data
    :return list of dict containing email data
    """
    return [
        {
            "subject": "I like tacos",
            "sender": "support@vestact.com",
            "recipient": "user@example.com",
            "body": "I'm quite partial to investing in large, founder-led businesses",
            "received_at": datetime(2025, 7, 6, 6, 57, 53),
        },
        {
            "subject": "Clear vision",
            "sender": "support@vestact.com",
            "recipient": "user@example.com",
            "body": " I was surprised to learn that there are now more listed ETFs than there are listed shares of companies in the US.",
            "received_at": datetime(2025, 9, 21, 7, 40, 16),
        },
        {
            "subject": "Green and gold ",
            "sender": "support@vestact.com",
            "recipient": "user@example.com",
            "body": "US markets opened weaker on Friday, extending Thursday's sell-off, but staged a solid intraday rebound",
            "received_at": datetime(2025, 11, 17, 8, 26, 9),
        }
    ]
