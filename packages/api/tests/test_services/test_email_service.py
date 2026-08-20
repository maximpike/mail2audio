from requests import Session
from services.email_service import EmailService


class TestEmailService:
    """
    Test suite for EmailService
    Tests the orchestration of parsing .eml files and persisting to database
    """

    def test_process_eml_file_success(self, test_db: Session, sample_eml_files):
        """Test that service can successfully process a valid .eml file"""
        # Arrange
        with open(sample_eml_files["tacos"], "rb") as f:
            eml_content = f.read()
        service = EmailService(test_db)

        # Act
        result = service.process_file(eml_content)

        # Asser

        # Assert
