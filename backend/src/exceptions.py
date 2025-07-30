"""Custom exceptions for the application."""


class PDFProcessingError(Exception):
    """Base exception for PDF processing errors."""
    pass


class InvalidFileTypeError(PDFProcessingError):
    """Raised when uploaded file is not a PDF."""
    pass


class FileSizeExceededError(PDFProcessingError):
    """Raised when uploaded file exceeds size limit."""
    pass


class PageLimitExceededError(PDFProcessingError):
    """Raised when PDF has too many pages."""
    pass


class PDFParsingError(PDFProcessingError):
    """Raised when PDF cannot be parsed."""
    pass


class OpenAIError(Exception):
    """Raised when OpenAI API fails."""
    pass


class SummaryNotFoundError(Exception):
    """Raised when requested summary doesn't exist."""
    pass