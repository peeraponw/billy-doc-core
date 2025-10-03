"""
Main FastAPI application for billy-doc-core.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from billy_doc_core.const import (
    API_DESCRIPTION,
    API_TITLE,
    API_VERSION,
    DEBUG,
    ENVIRONMENT,
    HOST,
    PORT,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print(f"Starting billy-doc-core {ENVIRONMENT} environment")
    print(f"Debug mode: {DEBUG}")

    # Initialize directories
    import os
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    yield

    # Shutdown
    print("Shutting down billy-doc-core")


# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version="0.1.0",
    debug=DEBUG,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "billy-doc-core",
        "version": "0.1.0",
        "status": "running",
        "environment": ENVIRONMENT,
        "docs_url": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2025-01-03T00:00:00Z",  # Would use real timestamp
        "version": "0.1.0",
    }


@app.get("/api/{api_version}/documents")
async def list_documents(api_version: str):
    """List all documents."""
    if api_version != API_VERSION:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API version {api_version} not found",
        )

    # TODO: Implement document listing
    return {
        "documents": [],
        "total": 0,
        "api_version": api_version,
    }


@app.post("/api/{api_version}/documents/generate")
async def generate_document(api_version: str):
    """Generate a new document."""
    if api_version != API_VERSION:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"API version {api_version} not found",
        )

    # TODO: Implement document generation
    return {
        "message": "Document generation not yet implemented",
        "api_version": api_version,
    }


if __name__ == "__main__":
    uvicorn.run(
        "src.billy_doc_core.main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info" if not DEBUG else "debug",
    )