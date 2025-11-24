"""
FastAPI Backend for Gemini File Search Starter

This API provides endpoints for:
- Uploading files to Gemini File Search Stores
- Querying files with natural language
- Managing File Search Stores
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional
import logging
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from gemini_client import GeminiFileSearchClient

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Gemini File Search API",
    description="API for uploading files and querying them with Gemini's File Search",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Next.js dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize storage directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize Gemini client
try:
    gemini_client = GeminiFileSearchClient()
    logger.info("Gemini client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini client: {e}")
    gemini_client = None


# Pydantic models for request/response validation
class QueryRequest(BaseModel):
    """Request model for querying files"""
    query: str = Field(..., description="The question to ask")
    store_name: str = Field(..., description="Name of the File Search Store")
    temperature: Optional[float] = Field(0.1, ge=0.0, le=1.0, description="Model temperature")


class Citation(BaseModel):
    """Citation information from File Search"""
    text: str = Field(..., description="Cited text snippet")
    source: str = Field(..., description="Source filename or identifier")
    uri: Optional[str] = Field(None, description="URI to the source")


class QueryResponse(BaseModel):
    """Response model for query results"""
    answer: str = Field(..., description="The model's answer")
    citations: List[Citation] = Field(default_factory=list, description="List of citations")


class FileInfo(BaseModel):
    """Information about an uploaded file"""
    name: str = Field(..., description="Name of the file")
    file_id: Optional[str] = Field(None, description="Gemini file ID")
    status: str = Field(..., description="Upload/indexing status")
    uploaded_at: str = Field(..., description="Upload timestamp")


class StoreInfo(BaseModel):
    """Information about a File Search Store"""
    name: str = Field(..., description="Store name/ID")
    display_name: str = Field(..., description="Human-readable store name")
    created_at: Optional[str] = Field(None, description="Creation timestamp")


class UploadResponse(BaseModel):
    """Response model for file upload"""
    success: bool
    message: str
    file_info: Optional[FileInfo] = None
    store_name: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "healthy",
        "service": "Gemini File Search API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    gemini_status = "connected" if gemini_client else "disconnected"
    from datetime import datetime, timezone
    return {
        "status": "healthy",
        "gemini": gemini_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    store_name: Optional[str] = Form(None),
    create_new_store: bool = Form(False)
):
    """
    Upload a file to a File Search Store.
    
    If store_name is not provided and create_new_store is False, 
    creates a default store or uses an existing one.
    """
    if not gemini_client:
        raise HTTPException(
            status_code=503,
            detail="Gemini client not initialized. Check GOOGLE_API_KEY."
        )
    
    try:
        # Save file locally
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File saved locally: {file_path}")
        
        # Determine or create store
        if create_new_store or not store_name:
            # Create a new store with timestamp
            from datetime import timezone
            display_name = f"FileSearchStore_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
            store = gemini_client.create_file_search_store(display_name=display_name)
            store_name = store["name"]
            logger.info(f"Created new store: {store_name}")
        
        # Detect MIME type
        mime_type = gemini_client.detect_mime_type(str(file_path))
        
        # Upload to Gemini File Search Store
        uploaded_file = gemini_client.upload_file_to_store(
            file_path=str(file_path),
            store_name=store_name,
            mime_type=mime_type
        )
        
        file_info = FileInfo(
            name=file.filename,
            file_id=uploaded_file.name,
            status="ready",
            uploaded_at=datetime.now(timezone.utc).isoformat()
        )
        
        return UploadResponse(
            success=True,
            message=f"File '{file.filename}' uploaded successfully",
            file_info=file_info,
            store_name=store_name
        )
        
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_files(request: QueryRequest):
    """
    Query files in a File Search Store using natural language.
    
    The model will search through all files in the store and return
    an answer with citations.
    """
    if not gemini_client:
        raise HTTPException(
            status_code=503,
            detail="Gemini client not initialized. Check GOOGLE_API_KEY."
        )
    
    try:
        logger.info(f"Processing query: {request.query[:100]}...")
        
        # Query with File Search
        result = gemini_client.query_with_file_search(
            query=request.query,
            store_name=request.store_name,
            temperature=request.temperature
        )
        
        # Convert citations to Pydantic models
        citations = [
            Citation(
                text=citation.get("text", ""),
                source=citation.get("source", "Unknown"),
                uri=citation.get("uri")
            )
            for citation in result.get("citations", [])
        ]
        
        return QueryResponse(
            answer=result.get("answer", "No answer generated"),
            citations=citations
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stores/list", response_model=List[StoreInfo])
async def list_stores():
    """
    List all File Search Stores.
    """
    if not gemini_client:
        raise HTTPException(
            status_code=503,
            detail="Gemini client not initialized. Check GOOGLE_API_KEY."
        )
    
    try:
        stores = gemini_client.list_stores()
        
        store_infos = []
        for store in stores:
            store_info = StoreInfo(
                name=store.get("name", ""),
                display_name=store.get("display_name", store.get("name", "")),
                created_at=store.get("created_at")
            )
            store_infos.append(store_info)
        
        return store_infos
        
    except Exception as e:
        logger.error(f"Error listing stores: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/stores/{store_id:path}")
async def delete_store(store_id: str):
    """
    Delete a File Search Store.
    
    Note: store_id should be in format "file_search_stores/{id}"
    """
    if not gemini_client:
        raise HTTPException(
            status_code=503,
            detail="Gemini client not initialized. Check GOOGLE_API_KEY."
        )
    
    try:
        # Construct full store name if needed
        if not store_id.startswith("file_search_stores/"):
            store_name = f"file_search_stores/{store_id}"
        else:
            store_name = store_id
        
        gemini_client.delete_store(store_name)
        
        return {
            "success": True,
            "message": f"Store '{store_name}' deleted successfully"
        }
        
    except Exception as e:
        logger.error(f"Error deleting store: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/supported-types")
async def get_supported_types():
    """
    Get list of supported file types.
    """
    if not gemini_client:
        raise HTTPException(
            status_code=503,
            detail="Gemini client not initialized. Check GOOGLE_API_KEY."
        )
    
    mime_types = gemini_client.get_supported_mime_types()
    
    return {
        "supported_extensions": list(mime_types.keys()),
        "mime_types": mime_types
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            detail=str(exc)
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).model_dump()
    )


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
