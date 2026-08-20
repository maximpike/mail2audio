"""
Root conftest.py - Shared fixtures for entire test suite
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.main import app
from app.models.base import Base


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


@pytest.fixture(scope="function")
def test_engine():
    """In-memory SQLite engine, rebuilt per test for a clean schema."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=False,
    )
    # SQLite ignores FK constraints unless asked; without this, cascade
    # and FK-integrity tests would silently pass against nothing.
    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys=ON"))
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(test_engine) -> Generator[Session, None, None]:
    """SQLAlchemy session bound to the in-memory engine."""
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = testing_session()
    session.execute(text("PRAGMA foreign_keys=ON"))
    try:
        yield session
    finally:
        session.rollback()
        session.close()
