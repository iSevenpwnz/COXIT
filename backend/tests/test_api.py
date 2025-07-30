"""Tests for API routes."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO

from app import app
from src.models import PDFMetadata
from src.exceptions import (
    PDFProcessingError,
    OpenAIError,
    DuplicateFileError,
    SummaryNotFoundError
)


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestAPI:
    """Test suite for API routes."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_get_history_empty(self, client):
        """Test history endpoint with empty history."""
        with patch('src.api.routes.StorageService.get_recent_history') as mock_history:
            mock_history.return_value = []
            
            response = client.get("/history")
            assert response.status_code == 200
            assert response.json() == {"history": []}

    def test_get_history_with_data(self, client):
        """Test history endpoint with data."""
        mock_metadata = PDFMetadata(
            id="test-id",
            filename="test.pdf",
            original_filename="original.pdf",
            file_hash="hash123",
            summary_file="test.txt",
            created_at="2025-01-01T00:00:00",
            pages=10,
            size_mb=1.5,
            text_length=1000,
            images=2,
            tables=1
        )
        
        with patch('src.api.routes.StorageService.get_recent_history') as mock_history:
            mock_history.return_value = [mock_metadata]
            
            response = client.get("/history")
            assert response.status_code == 200
            
            data = response.json()
            assert len(data["history"]) == 1
            assert data["history"][0]["id"] == "test-id"
            assert data["history"][0]["original_filename"] == "original.pdf"

    def test_get_history_error(self, client):
        """Test history endpoint with error."""
        with patch('src.api.routes.StorageService.get_recent_history') as mock_history:
            mock_history.side_effect = Exception("Database error")
            
            response = client.get("/history")
            assert response.status_code == 500
            assert "Failed to retrieve history" in response.json()["detail"]

    def test_download_summary_success(self, client):
        """Test successful summary download."""
        with patch('src.api.routes.StorageService.get_summary') as mock_get_summary:
            mock_get_summary.return_value = "Test summary content"
            
            response = client.get("/download/test-id")
            assert response.status_code == 200
            assert response.json() == {"summary": "Test summary content"}

    def test_download_summary_not_found(self, client):
        """Test summary download when not found."""
        with patch('src.api.routes.StorageService.get_summary') as mock_get_summary:
            mock_get_summary.side_effect = SummaryNotFoundError("Summary not found")
            
            response = client.get("/download/test-id")
            assert response.status_code == 404
            assert "Summary not found" in response.json()["detail"]

    def test_upload_pdf_success(self, client):
        """Test successful PDF upload."""
        # Create a mock PDF file
        pdf_content = b"Mock PDF content"
        files = {"file": ("test.pdf", BytesIO(pdf_content), "application/pdf")}
        
        with patch('src.api.routes.PDFService.calculate_file_hash') as mock_hash, \
             patch('src.api.routes.StorageService.check_duplicate_file') as mock_duplicate, \
             patch('src.api.routes.PDFService.validate_upload') as mock_validate, \
             patch('src.api.routes.PDFService.save_pdf') as mock_save, \
             patch('src.api.routes.PDFService.parse_pdf') as mock_parse, \
             patch('src.api.routes.AIService') as mock_ai_service, \
             patch('src.api.routes.StorageService.save_summary') as mock_save_summary, \
             patch('src.api.routes.StorageService.create_metadata') as mock_create_meta, \
             patch('src.api.routes.StorageService.save_metadata') as mock_save_meta:
            
            # Setup mocks
            mock_hash.return_value = "test-hash"
            mock_duplicate.return_value = None
            mock_validate.return_value = 10
            mock_save.return_value = ("test-id", "test-path")
            
            mock_parse_result = Mock()
            mock_parse_result.text = "Extracted text"
            mock_parse_result.images = 2
            mock_parse_result.tables = 1
            mock_parse.return_value = mock_parse_result
            
            mock_ai_instance = Mock()
            mock_ai_instance.generate_summary.return_value = "AI generated summary"
            mock_ai_service.return_value = mock_ai_instance
            
            mock_metadata = Mock()
            mock_create_meta.return_value = mock_metadata
            
            response = client.post("/upload", files=files)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "test-id"
            assert data["pages"] == 10
            assert data["summary"] == "AI generated summary"

    def test_upload_pdf_duplicate(self, client):
        """Test PDF upload with duplicate file."""
        pdf_content = b"Mock PDF content"
        files = {"file": ("test.pdf", BytesIO(pdf_content), "application/pdf")}
        
        mock_existing = PDFMetadata(
            id="existing-id",
            filename="existing.pdf",
            original_filename="existing.pdf",
            file_hash="test-hash",
            summary_file="existing.txt",
            created_at="2025-01-01T00:00:00",
            pages=10,
            size_mb=1.0,
            text_length=100,
            images=1,
            tables=0
        )
        
        with patch('src.api.routes.PDFService.calculate_file_hash') as mock_hash, \
             patch('src.api.routes.StorageService.check_duplicate_file') as mock_duplicate:
            
            mock_hash.return_value = "test-hash"
            mock_duplicate.return_value = mock_existing
            
            response = client.post("/upload", files=files)
            
            assert response.status_code == 409
            assert "already exists" in response.json()["detail"]

    def test_upload_pdf_invalid_file_type(self, client):
        """Test PDF upload with invalid file type."""
        text_content = b"This is not a PDF"
        files = {"file": ("test.txt", BytesIO(text_content), "text/plain")}
        
        with patch('src.api.routes.PDFService.calculate_file_hash') as mock_hash, \
             patch('src.api.routes.StorageService.check_duplicate_file') as mock_duplicate, \
             patch('src.api.routes.PDFService.validate_upload') as mock_validate:
            
            mock_hash.return_value = "test-hash"
            mock_duplicate.return_value = None
            mock_validate.side_effect = PDFProcessingError("Invalid file type")
            
            response = client.post("/upload", files=files)
            
            assert response.status_code == 400
            assert "Invalid file type" in response.json()["detail"]

    def test_upload_pdf_ai_error(self, client):
        """Test PDF upload with AI service error."""
        pdf_content = b"Mock PDF content"
        files = {"file": ("test.pdf", BytesIO(pdf_content), "application/pdf")}
        
        with patch('src.api.routes.PDFService.calculate_file_hash') as mock_hash, \
             patch('src.api.routes.StorageService.check_duplicate_file') as mock_duplicate, \
             patch('src.api.routes.PDFService.validate_upload') as mock_validate, \
             patch('src.api.routes.PDFService.save_pdf') as mock_save, \
             patch('src.api.routes.PDFService.parse_pdf') as mock_parse, \
             patch('src.api.routes.AIService') as mock_ai_service:
            
            mock_hash.return_value = "test-hash"
            mock_duplicate.return_value = None
            mock_validate.return_value = 10
            mock_save.return_value = ("test-id", "test-path")
            
            mock_parse_result = Mock()
            mock_parse_result.text = "Extracted text"
            mock_parse.return_value = mock_parse_result
            
            mock_ai_instance = Mock()
            mock_ai_instance.generate_summary.side_effect = OpenAIError("AI service failed")
            mock_ai_service.return_value = mock_ai_instance
            
            response = client.post("/upload", files=files)
            
            assert response.status_code == 500
            assert "AI service failed" in response.json()["detail"]