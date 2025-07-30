"""PDF processing service."""
import uuid
from io import BytesIO
from pathlib import Path
from typing import BinaryIO

import fitz  # PyMuPDF
import pdfplumber
from PyPDF2 import PdfReader
from fastapi import UploadFile

from ..config import settings
from ..exceptions import (
    InvalidFileTypeError, 
    FileSizeExceededError, 
    PageLimitExceededError, 
    PDFParsingError
)
from ..models import PDFParseResult


class PDFService:
    """Service for handling PDF operations."""
    
    @staticmethod
    def validate_upload(file: UploadFile, contents: bytes) -> int:
        """Validate uploaded PDF file.
        
        Args:
            file: The uploaded file
            contents: File contents as bytes
            
        Returns:
            Number of pages in the PDF
            
        Raises:
            InvalidFileTypeError: If file is not a PDF
            FileSizeExceededError: If file exceeds size limit
            PageLimitExceededError: If PDF has too many pages
            PDFParsingError: If PDF cannot be read
        """
        # Validate file type
        if file.content_type != "application/pdf":
            raise InvalidFileTypeError("Only PDF files are supported")
        
        # Validate file size
        size_mb = len(contents) / (1024 * 1024)
        if size_mb > settings.MAX_FILE_SIZE_MB:
            raise FileSizeExceededError(f"PDF file too large (max {settings.MAX_FILE_SIZE_MB}MB)")
        
        # Validate page count
        try:
            reader = PdfReader(BytesIO(contents))
            num_pages = len(reader.pages)
        except Exception as e:
            raise PDFParsingError(f"Cannot read PDF file: {str(e)}")
            
        if num_pages > settings.MAX_PAGES:
            raise PageLimitExceededError(f"PDF has too many pages (max {settings.MAX_PAGES})")
        
        return num_pages
    
    @staticmethod
    def parse_pdf(file_path: Path) -> PDFParseResult:
        """Parse PDF file to extract text, images, and tables.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            PDFParseResult with extracted content information
        """
        # Extract text
        text = PDFService._extract_text(file_path)
        
        # Count images
        images_count = PDFService._count_images(file_path)
        
        # Count tables
        tables_count = PDFService._count_tables(file_path)
        
        return PDFParseResult(
            text=text,
            images=images_count,
            tables=tables_count
        )
    
    @staticmethod
    def save_pdf(contents: bytes) -> tuple[str, Path]:
        """Save PDF contents to storage.
        
        Args:
            contents: PDF file contents
            
        Returns:
            Tuple of (file_id, file_path)
        """
        file_id = str(uuid.uuid4())
        file_path = settings.PDFS_DIR / f"{file_id}.pdf"
        
        with open(file_path, "wb") as f:
            f.write(contents)
            
        return file_id, file_path
    
    @staticmethod
    def _extract_text(file_path: Path) -> str:
        """Extract text from PDF using pdfplumber."""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
        except Exception:
            # Silently fail and return empty text
            pass
        return text
    
    @staticmethod
    def _count_images(file_path: Path) -> int:
        """Count images in PDF using PyMuPDF."""
        images_count = 0
        try:
            doc = fitz.open(file_path)
            for page in doc:
                images_count += len(page.get_images(full=True))
            doc.close()
        except Exception:
            # Silently fail and return 0
            pass
        return images_count
    
    @staticmethod
    def _count_tables(file_path: Path) -> int:
        """Count tables in PDF using pdfplumber."""
        tables_count = 0
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    if tables:
                        tables_count += len(tables)
        except Exception:
            # Silently fail and return 0
            pass
        return tables_count