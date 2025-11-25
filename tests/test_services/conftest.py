"""
Service layer fixture - Mocked dependencies
"""
import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock, MagicMock
from pathlib import Path


@pytest.fixture
def sample_eml_files():
    """ Load .eml files from upload directory """
    # Get the project root directory (assuming tests/ is at project root)
    project_root = Path(__file__).parent.parent.parent
    email_examples_dir = project_root / "docs" / "email-examples"
    return {
        "tacos": email_examples_dir / "I_like_tacos.eml",
        "vision": email_examples_dir / "Clear_vision.eml",
        "gold": email_examples_dir / "Green_and_gold.eml"
    }

@pytest.fixture
def mock_email_repository(mocker: MockerFixture) -> Mock:
    """
    Mock repository for email service tests.
    Uses pytest-mock for cleaner syntax
    """
    mock_repo = mocker.Mock()
    # Set up common return values
    mock_repo.get_by_id.return_value = None
    mock_repo.save.return_value = Mock(id=1)
    return mock_repo

@pytest.fixture
def mock_parser_service(mocker: MockerFixture) -> Mock:
    """
    Mock parser service for email processing.
    """
    mock_parser = mocker.Mock()
    mock_parser.pase_html.return_value = {
        "subject": "Newsletter Title",
        "body": "Clean parsed content here..."
    }
    return mock_parser