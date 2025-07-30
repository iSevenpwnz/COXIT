"""Tests for PDF service."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO

from fastapi import UploadFile

from src.services.pdf_service import PDFService
from src.exceptions import (
    InvalidFileTypeError,
    FileSizeExceededError,
    PageLimitExceededError,
    PDFParsingError,
)


class TestPDFService:
    """Test suite for PDFService."""

    def test_calculate_file_hash(self):
        """Test file hash calculation."""
        test_content = b"test content"
        hash_result = PDFService.calculate_file_hash(test_content)

        # SHA-256 of "test content"
        expected_hash = (
            "6ae8a75555209fd6c44157c0aed8016e763ff435a19cf186f76863140143ff72"
        )
        assert hash_result == expected_hash

    def test_validate_upload_invalid_content_type(self):
        """Test validation with invalid content type."""
        mock_file = Mock(spec=UploadFile)
        mock_file.content_type = "text/plain"

        with pytest.raises(
            InvalidFileTypeError, match="Only PDF files are supported"
        ):
            PDFService.validate_upload(mock_file, b"content")

    def test_validate_upload_file_too_large(self):
        """Test validation with oversized file."""
        mock_file = Mock(spec=UploadFile)
        mock_file.content_type = "application/pdf"

        # Create content larger than 50MB
        large_content = b"x" * (51 * 1024 * 1024)

        with pytest.raises(FileSizeExceededError, match="PDF file too large"):
            PDFService.validate_upload(mock_file, large_content)

    @patch("src.services.pdf_service.PdfReader")
    def test_validate_upload_too_many_pages(self, mock_reader):
        """Test validation with too many pages."""
        mock_file = Mock(spec=UploadFile)
        mock_file.content_type = "application/pdf"

        # Mock PDF with 101 pages
        mock_pdf = Mock()
        mock_pdf.pages = [Mock()] * 101
        mock_reader.return_value = mock_pdf

        small_content = b"small pdf content"

        with pytest.raises(
            PageLimitExceededError, match="PDF has too many pages"
        ):
            PDFService.validate_upload(mock_file, small_content)

    @patch("src.services.pdf_service.PdfReader")
    def test_validate_upload_parsing_error(self, mock_reader):
        """Test validation with PDF parsing error."""
        mock_file = Mock(spec=UploadFile)
        mock_file.content_type = "application/pdf"

        mock_reader.side_effect = Exception("PDF parsing failed")

        with pytest.raises(PDFParsingError, match="Cannot read PDF file"):
            PDFService.validate_upload(mock_file, b"content")

    @patch("src.services.pdf_service.PdfReader")
    def test_validate_upload_success(self, mock_reader):
        """Test successful validation."""
        mock_file = Mock(spec=UploadFile)
        mock_file.content_type = "application/pdf"

        # Mock PDF with 10 pages
        mock_pdf = Mock()
        mock_pdf.pages = [Mock()] * 10
        mock_reader.return_value = mock_pdf

        content = b"valid pdf content"

        result = PDFService.validate_upload(mock_file, content)
        assert result == 10

    @patch("src.services.pdf_service.settings")
    @patch("builtins.open", new_callable=MagicMock)
    def test_save_pdf(self, mock_open, mock_settings):
        """Test PDF saving."""
        mock_settings.PDFS_DIR = Path("/test/pdfs")

        content = b"pdf content"
        file_id, file_path = PDFService.save_pdf(content)

        # Check that file_id is a valid UUID string
        assert len(file_id) == 36
        assert isinstance(file_path, Path)
        assert file_path.name.endswith(".pdf")

        # Check that file was written
        mock_open.assert_called_once()
        mock_open().__enter__().write.assert_called_once_with(content)

    @patch("src.services.pdf_service.pdfplumber.open")
    def test_extract_text_success(self, mock_pdfplumber):
        """Test text extraction success."""
        # Mock pdfplumber
        mock_page = Mock()
        mock_page.extract_text.return_value = "Test page content"

        mock_pdf = Mock()
        mock_pdf.pages = [mock_page, mock_page]
        mock_pdf.__enter__ = Mock(return_value=mock_pdf)
        mock_pdf.__exit__ = Mock(return_value=None)

        mock_pdfplumber.return_value = mock_pdf

        result = PDFService._extract_text(Path("test.pdf"))
        assert result == "Test page contentTest page content"

    @patch("src.services.pdf_service.pdfplumber.open")
    def test_extract_text_failure(self, mock_pdfplumber):
        """Test text extraction failure."""
        mock_pdfplumber.side_effect = Exception("Extraction failed")

        result = PDFService._extract_text(Path("test.pdf"))
        assert result == ""

    @patch("src.services.pdf_service.fitz.open")
    def test_count_images_success(self, mock_fitz):
        """Test image counting success."""
        mock_page = Mock()
        mock_page.get_images.return_value = ["img1", "img2", "img3"]

        mock_doc = Mock()
        mock_doc.__iter__ = Mock(return_value=iter([mock_page, mock_page]))
        mock_doc.close = Mock()

        mock_fitz.return_value = mock_doc

        result = PDFService._count_images(Path("test.pdf"))
        assert result == 6  # 3 images per page * 2 pages

    @patch("src.services.pdf_service.fitz.open")
    def test_count_images_failure(self, mock_fitz):
        """Test image counting failure."""
        mock_fitz.side_effect = Exception("Counting failed")

        result = PDFService._count_images(Path("test.pdf"))
        assert result == 0

    @patch("src.services.pdf_service.pdfplumber.open")
    def test_count_tables_success(self, mock_pdfplumber):
        """Test table counting success."""
        mock_page = Mock()
        mock_page.extract_tables.return_value = [["table1"], ["table2"]]

        mock_pdf = Mock()
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__ = Mock(return_value=mock_pdf)
        mock_pdf.__exit__ = Mock(return_value=None)

        mock_pdfplumber.return_value = mock_pdf

        result = PDFService._count_tables(Path("test.pdf"))
        assert result == 2

    @patch("src.services.pdf_service.PDFService._count_tables")
    @patch("src.services.pdf_service.PDFService._count_images")
    @patch("src.services.pdf_service.PDFService._extract_text")
    def test_parse_pdf(
        self, mock_extract_text, mock_count_images, mock_count_tables
    ):
        """Test complete PDF parsing."""
        mock_extract_text.return_value = "Extracted text"
        mock_count_images.return_value = 5
        mock_count_tables.return_value = 2

        result = PDFService.parse_pdf(Path("test.pdf"))

        assert result.text == "Extracted text"
        assert result.images == 5
        assert result.tables == 2
