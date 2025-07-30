"""Data models and schemas."""
from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator


class PDFMetadata(BaseModel):
    """PDF file metadata model."""
    id: str
    filename: str
    original_filename: str
    file_hash: str
    summary_file: str
    created_at: str
    pages: int
    size_mb: float
    text_length: int
    images: int
    tables: int
    
    @model_validator(mode='before')
    @classmethod
    def set_defaults(cls, data):
        """Set defaults for backward compatibility."""
        if isinstance(data, dict):
            if 'original_filename' not in data:
                data['original_filename'] = data.get('filename', 'unknown.pdf')
            if 'file_hash' not in data:
                data['file_hash'] = 'legacy'
        return data


class PDFParseResult(BaseModel):
    """Result of PDF parsing operation."""
    text: str
    images: int
    tables: int


class UploadResponse(BaseModel):
    """Response model for successful PDF upload."""
    id: str
    pages: int
    size_mb: float = Field(..., ge=0)
    text_length: int = Field(..., ge=0)
    images: int = Field(..., ge=0)
    tables: int = Field(..., ge=0)
    summary: str


class HistoryResponse(BaseModel):
    """Response model for history endpoint."""
    history: list[PDFMetadata]


class SummaryResponse(BaseModel):
    """Response model for summary download."""
    summary: str


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = "ok"