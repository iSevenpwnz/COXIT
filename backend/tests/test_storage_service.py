"""Tests for Storage service."""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from src.services.storage_service import StorageService
from src.models import PDFMetadata
from src.exceptions import SummaryNotFoundError


class TestStorageService:
    """Test suite for StorageService."""

    @patch('src.services.storage_service.settings')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_summary(self, mock_file, mock_settings):
        """Test summary saving."""
        mock_settings.SUMMARIES_DIR = Path("/test/summaries")

        file_id = "test-id"
        summary = "Test summary content"

        result = StorageService.save_summary(file_id, summary)

        expected_path = Path("/test/summaries") / f"{file_id}.txt"
        assert result == expected_path

        mock_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
        mock_file().write.assert_called_once_with(summary)

    @patch('json.dump')
    @patch('src.services.storage_service.StorageService._load_all_metadata')
    @patch('src.services.storage_service.settings')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_metadata(self, mock_file, mock_settings, mock_load, mock_json_dump):
        """Test metadata saving."""
        mock_settings.META_FILE = Path("/test/metadata.json")
        mock_settings.MAX_HISTORY_ITEMS = 1000

        existing_metadata = [{"id": "old-id", "filename": "old.pdf"}]
        mock_load.return_value = existing_metadata

        new_metadata = PDFMetadata(
            id="new-id",
            filename="new.pdf",
            original_filename="original.pdf",
            file_hash="hash123",
            summary_file="new.txt",
            created_at="2025-01-01T00:00:00",
            pages=10,
            size_mb=1.5,
            text_length=1000,
            images=2,
            tables=1
        )

        StorageService.save_metadata(new_metadata)

        mock_file.assert_called_once_with(mock_settings.META_FILE, "w", encoding="utf-8")

        args, _ = mock_json_dump.call_args
        written_data = args[0]

        assert isinstance(written_data, list)
        assert len(written_data) == 2
        assert written_data[1]["id"] == "new-id"

    @patch('src.services.storage_service.settings')
    def test_get_summary_success(self, mock_settings):
        """Test successful summary retrieval."""
        mock_settings.SUMMARIES_DIR = Path("/test/summaries")

        summary_content = "Test summary"
        summary_path = Path("/test/summaries/test-id.txt")

        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=summary_content)):

            result = StorageService.get_summary("test-id")
            assert result == summary_content

    @patch('src.services.storage_service.settings')
    def test_get_summary_not_found(self, mock_settings):
        """Test summary not found error."""
        mock_settings.SUMMARIES_DIR = Path("/test/summaries")

        with patch('pathlib.Path.exists', return_value=False):
            with pytest.raises(SummaryNotFoundError, match="Summary with ID test-id not found"):
                StorageService.get_summary("test-id")

    @patch('src.services.storage_service.StorageService._load_all_metadata')
    @patch('src.services.storage_service.settings')
    def test_get_recent_history(self, mock_settings, mock_load):
        """Test recent history retrieval."""
        mock_settings.HISTORY_DISPLAY_LIMIT = 2

        metadata = [
            {
                "id": "legacy-1",
                "filename": "legacy1.pdf",
                "summary_file": "legacy1.txt",
                "created_at": "2025-01-01T00:00:00",
                "pages": 10,
                "size_mb": 1.0,
                "text_length": 100,
                "images": 1,
                "tables": 0
            },
            {
                "id": "new-1",
                "filename": "new1.pdf",
                "original_filename": "original1.pdf",
                "file_hash": "hash123",
                "summary_file": "new1.txt",
                "created_at": "2025-01-02T00:00:00",
                "pages": 5,
                "size_mb": 0.5,
                "text_length": 50,
                "images": 0,
                "tables": 1
            },
            {
                "id": "new-2",
                "filename": "new2.pdf",
                "original_filename": "original2.pdf",
                "file_hash": "hash456",
                "summary_file": "new2.txt",
                "created_at": "2025-01-03T00:00:00",
                "pages": 8,
                "size_mb": 1.2,
                "text_length": 200,
                "images": 3,
                "tables": 2
            }
        ]
        mock_load.return_value = metadata

        result = StorageService.get_recent_history()

        assert len(result) == 2
        assert result[0].id == "new-2"
        assert result[1].id == "new-1"
        assert result[1].original_filename == "original1.pdf"
        assert result[1].file_hash == "hash123"

    @patch('src.services.storage_service.StorageService._load_all_metadata')
    def test_check_duplicate_file_found(self, mock_load):
        """Test duplicate file detection - found."""
        metadata = [
            {
                "id": "existing-id",
                "filename": "existing.pdf",
                "original_filename": "original.pdf",
                "file_hash": "duplicate-hash",
                "summary_file": "existing.txt",
                "created_at": "2025-01-01T00:00:00",
                "pages": 10,
                "size_mb": 1.0,
                "text_length": 100,
                "images": 1,
                "tables": 0
            }
        ]
        mock_load.return_value = metadata

        result = StorageService.check_duplicate_file("duplicate-hash")

        assert result is not None
        assert result.id == "existing-id"
        assert result.file_hash == "duplicate-hash"

    @patch('src.services.storage_service.StorageService._load_all_metadata')
    def test_check_duplicate_file_not_found(self, mock_load):
        """Test duplicate file detection - not found."""
        metadata = [
            {
                "id": "existing-id",
                "filename": "existing.pdf",
                "file_hash": "different-hash",
                "summary_file": "existing.txt",
                "created_at": "2025-01-01T00:00:00",
                "pages": 10,
                "size_mb": 1.0,
                "text_length": 100,
                "images": 1,
                "tables": 0
            }
        ]
        mock_load.return_value = metadata

        result = StorageService.check_duplicate_file("target-hash")
        assert result is None

    def test_create_metadata(self):
        """Test metadata creation."""
        with patch('src.services.storage_service.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value.isoformat.return_value = "2025-01-01T12:00:00"

            result = StorageService.create_metadata(
                file_id="test-id",
                filename="test.pdf",
                original_filename="original.pdf",
                file_hash="hash123",
                pages=10,
                size_mb=1.5,
                text_length=1000,
                images=2,
                tables=1
            )

            assert result.id == "test-id"
            assert result.filename == "test.pdf"
            assert result.original_filename == "original.pdf"
            assert result.file_hash == "hash123"
            assert result.summary_file == "test-id.txt"
            assert result.created_at == "2025-01-01T12:00:00"
            assert result.pages == 10
            assert result.size_mb == 1.5
            assert result.text_length == 1000
            assert result.images == 2
            assert result.tables == 1

    @patch('src.services.storage_service.settings')
    def test_load_all_metadata_file_not_exists(self, mock_settings):
        """Test loading metadata when file doesn't exist."""
        mock_settings.META_FILE = Path("/test/metadata.json")

        with patch('pathlib.Path.exists', return_value=False):
            result = StorageService._load_all_metadata()
            assert result == []

    @patch('src.services.storage_service.settings')
    def test_load_all_metadata_success(self, mock_settings):
        """Test successful metadata loading."""
        mock_settings.META_FILE = Path("/test/metadata.json")

        test_data = [{"id": "test", "filename": "test.pdf"}]

        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=json.dumps(test_data))):

            result = StorageService._load_all_metadata()
            assert result == test_data

    @patch('src.services.storage_service.settings')
    def test_load_all_metadata_json_error(self, mock_settings):
        """Test metadata loading with JSON error."""
        mock_settings.META_FILE = Path("/test/metadata.json")

        with patch('pathlib.Path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data="invalid json")):

            result = StorageService._load_all_metadata()
            assert result == []
