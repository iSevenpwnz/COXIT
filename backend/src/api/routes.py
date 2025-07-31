"""API routes for the PDF Summary application."""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse

from ..models import UploadResponse, HistoryResponse, SummaryResponse, HealthResponse
from ..services.pdf_service import PDFService
from ..services.ai_service import AIService
from ..services.storage_service import StorageService
from ..exceptions import (
    PDFProcessingError,
    OpenAIError,
    SummaryNotFoundError,
    DuplicateFileError
)

router = APIRouter()


def get_ai_service() -> AIService:
    """Dependency to get AI service instance."""
    return AIService()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    ai_service: AIService = Depends(get_ai_service)
) -> UploadResponse:
    """Upload and process a PDF file.
    
    Args:
        file: The uploaded PDF file
        ai_service: AI service for generating summaries
        
    Returns:
        Processing results including summary
        
    Raises:
        HTTPException: For various validation and processing errors
    """
    try:
        # Read file contents
        contents = await file.read()
        
        # Calculate file hash for duplicate detection
        file_hash = PDFService.calculate_file_hash(contents)
        
        # Check for duplicates
        existing_file = StorageService.check_duplicate_file(file_hash)
        if existing_file:
            raise DuplicateFileError(
                f"File '{existing_file.original_filename}' already exists. "
                f"Uploaded on {existing_file.created_at[:19].replace('T', ' ')}"
            )
        
        # Validate the upload
        num_pages = PDFService.validate_upload(file, contents)
        
        # Save PDF file
        file_id, file_path = PDFService.save_pdf(contents)
        
        # Parse PDF content
        parse_result = PDFService.parse_pdf(file_path)
        
        # Generate AI summary
        summary = ai_service.generate_summary(parse_result.text)
        
        # Save summary
        StorageService.save_summary(file_id, summary)
        
        # Create and save metadata
        size_mb = round(len(contents) / (1024 * 1024), 2)
        metadata = StorageService.create_metadata(
            file_id=file_id,
            filename=f"{file_id}.pdf",
            original_filename=file.filename or "unknown.pdf",
            file_hash=file_hash,
            pages=num_pages,
            size_mb=size_mb,
            text_length=len(parse_result.text),
            images=parse_result.images,
            tables=parse_result.tables
        )
        StorageService.save_metadata(metadata)
        
        return UploadResponse(
            id=file_id,
            pages=num_pages,
            size_mb=size_mb,
            text_length=len(parse_result.text),
            images=parse_result.images,
            tables=parse_result.tables,
            summary=summary
        )
        
    except DuplicateFileError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except PDFProcessingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/history", response_model=HistoryResponse)
async def get_history() -> HistoryResponse:
    """Get recent processing history.
    
    Returns:
        List of recently processed PDFs
    """
    try:
        history = StorageService.get_recent_history()
        return HistoryResponse(history=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")


@router.get("/download/{summary_id}", response_model=SummaryResponse)
async def download_summary(summary_id: str) -> JSONResponse:
    """Download summary by ID.
    
    Args:
        summary_id: ID of the summary to download
        
    Returns:
        Summary content
        
    Raises:
        HTTPException: If summary not found
    """
    try:
        summary = StorageService.get_summary(summary_id)
        return JSONResponse(content={"summary": summary})
    except SummaryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve summary: {str(e)}")