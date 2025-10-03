"""
Constants and configuration for billy-doc-core.
"""

import os
from typing import Final

# API Configuration
API_VERSION: Final[str] = "v1"
API_TITLE: Final[str] = "Billy Document Core API"
API_DESCRIPTION: Final[str] = "Open source document generation engine with Thai language support"

# Document Types
DOCUMENT_TYPES: Final[list[str]] = ["quotation", "invoice", "receipt"]

# Supported Languages
SUPPORTED_LANGUAGES: Final[list[str]] = ["th", "en"]

# Thai Language Configuration
THAI_FONTS: Final[list[str]] = ["TH Sarabun New", "TH SarabunPSK", "Tahoma", "Cordia New"]
DEFAULT_THAI_FONT: Final[str] = "TH Sarabun New"

# File Storage Configuration
UPLOAD_DIR: Final[str] = "uploads"
OUTPUT_DIR: Final[str] = "output"
MAX_FILE_SIZE: Final[int] = 10 * 1024 * 1024  # 10MB

# Performance Configuration
DEFAULT_TIMEOUT: Final[int] = 30  # seconds
MAX_CONCURRENT_REQUESTS: Final[int] = 10

# Environment-based configuration
DEBUG: Final[bool] = os.getenv("DEBUG", "false").lower() == "true"
ENVIRONMENT: Final[str] = os.getenv("ENVIRONMENT", "development")

# Server Configuration
HOST: Final[str] = os.getenv("HOST", "0.0.0.0")
PORT: Final[int] = int(os.getenv("PORT", "8000"))

# Security
SECRET_KEY: Final[str] = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
API_KEY_HEADER: Final[str] = "X-API-Key"

# Thai Business Constants
THAI_BAHT_CURRENCY: Final[str] = "THB"
MAX_THAI_AMOUNT: Final[int] = 1_000_000_000  # 1 billion Baht