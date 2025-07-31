"""Storage service for managing files and metadata."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from ..config import settings
from ..exceptions import SummaryNotFoundError, DuplicateFileError
from ..models import PDFMetadata


class StorageService:
    """Service for handling file storage and metadata operations."""

    @staticmethod
    def save_summary(file_id: str, summary: str) -> Path:
        """Save summary to storage.

        Args:
            file_id: Unique identifier for the file
            summary: Summary text to save

        Returns:
            Path to the saved summary file
        """
        summary_path = settings.SUMMARIES_DIR / f"{file_id}.txt"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        return summary_path

    @staticmethod
    def save_metadata(metadata: PDFMetadata) -> None:
        """Save metadata to the metadata file.

        Args:
            metadata: PDF metadata to save
        """
        # Load existing metadata
        all_metadata = StorageService._load_all_metadata()

        # Add new metadata
        all_metadata.append(metadata.model_dump())

        # Keep only the last N items
        all_metadata = all_metadata[-settings.MAX_HISTORY_ITEMS :]

        # Save back to file
        with open(settings.META_FILE, "w", encoding="utf-8") as f:
            json.dump(all_metadata, f, ensure_ascii=False, indent=2)

    @staticmethod
    def get_recent_history() -> List[PDFMetadata]:
        """Get recent processing history.

        Returns:
            List of recent PDF metadata, most recent first
        """
        all_metadata = StorageService._load_all_metadata()

        # Get last N items and reverse for most recent first
        recent_items = all_metadata[-settings.HISTORY_DISPLAY_LIMIT :][::-1]

        # Convert to PDFMetadata with backward compatibility
        result = []
        for item in recent_items:
            try:
                result.append(PDFMetadata(**item))
            except Exception as e:
                # Skip invalid items
                print(f"Skipping invalid metadata item: {e}")
                continue

        return result

    @staticmethod
    def get_summary(summary_id: str) -> str:
        """Get summary by ID.

        Args:
            summary_id: ID of the summary to retrieve

        Returns:
            Summary text

        Raises:
            SummaryNotFoundError: If summary file doesn't exist
        """
        summary_path = settings.SUMMARIES_DIR / f"{summary_id}.txt"

        if not summary_path.exists():
            raise SummaryNotFoundError(
                f"Summary with ID {summary_id} not found"
            )

        with open(summary_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def check_duplicate_file(file_hash: str) -> Optional[PDFMetadata]:
        """Check if file with this hash already exists.

        Args:
            file_hash: SHA-256 hash of the file

        Returns:
            PDFMetadata if duplicate found, None otherwise
        """
        all_metadata = StorageService._load_all_metadata()

        for item in all_metadata:
            if item.get("file_hash") == file_hash:
                try:
                    return PDFMetadata(**item)
                except Exception:
                    # Skip invalid item
                    continue

        return None

    @staticmethod
    def create_metadata(
        file_id: str,
        filename: str,
        original_filename: str,
        file_hash: str,
        pages: int,
        size_mb: float,
        text_length: int,
        images: int,
        tables: int,
    ) -> PDFMetadata:
        """Create metadata object for a processed PDF.

        Args:
            file_id: Unique file identifier
            pages: Number of pages
            size_mb: File size in MB
            text_length: Length of extracted text
            images: Number of images
            tables: Number of tables

        Returns:
            PDFMetadata object
        """
        return PDFMetadata(
            id=file_id,
            filename=filename,
            original_filename=original_filename,
            file_hash=file_hash,
            summary_file=f"{file_id}.txt",
            created_at=datetime.utcnow().isoformat(),
            pages=pages,
            size_mb=size_mb,
            text_length=text_length,
            images=images,
            tables=tables,
        )

    @staticmethod
    def _load_all_metadata() -> List[dict]:
        """Load all metadata from file.

        Returns:
            List of metadata dictionaries
        """
        if not settings.META_FILE.exists():
            return []

        try:
            with open(settings.META_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
