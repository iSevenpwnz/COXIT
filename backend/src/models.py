"""Data models and schemas."""
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel, Field


class PDFMetadata(BaseModel):
    """PDF file metadata model."""
    id: str
    filename: str
    summary_file: str
    created_at: str
    pages: int
    size_mb: float
    text_length: int
    images: int
    tables: int


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