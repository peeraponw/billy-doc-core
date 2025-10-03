# billy-doc-core

Open source document generation engine with Thai language support for business documents (quotations, invoices, receipts).

## Overview

billy-doc-core is the open source backend service that provides PDF document generation capabilities with comprehensive Thai language support. It serves as the foundation for the Billy Document Application ecosystem.

## Features

- **Thai Language Support**: Full Thai text processing and PDF generation
- **Multiple Document Types**: Quotation, Invoice, and Receipt generation
- **FastAPI Backend**: Modern, fast web framework with automatic API documentation
- **WeasyPrint Integration**: High-quality PDF generation with Thai font support
- **RESTful API**: Clean API design for easy integration

## Technology Stack

- **Python 3.13+** with **UV** package management
- **FastAPI** for the web framework
- **Pydantic** for data validation
- **WeasyPrint** for PDF generation
- **pytest** for testing

## Quick Start

### Prerequisites

- Python 3.13+
- UV package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd billy-doc-core

# Install dependencies
uv sync

# Run in development mode
uv run uvicorn src.billy_doc_core.main:app --reload
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

### Production Deployment (Open Source)

For production deployment, you can use Docker/Podman:

```bash
# Build Docker image
docker build -t billy-doc-core .

# Run with Docker
docker run -p 8000:8000 billy-doc-core

# Or use Podman (daemonless)
podman build -t billy-doc-core .
podman run -p 8000:8000 billy-doc-core
```

For cloud deployment, see the [billy-doc-saas](https://github.com/your-org/billy-doc-saas) repository which includes infrastructure as code for production deployment.

## API Endpoints

- `GET /` - Root endpoint with service information
- `GET /health` - Health check endpoint
- `GET /api/v1/documents` - List documents
- `POST /api/v1/documents/generate` - Generate new document

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src
```

### Code Quality

```bash
# Format code
uv run ruff format src/

# Lint code
uv run ruff check src/
```

## Architecture

This repository follows the UV build standard with the main package located in `src/billy_doc_core/`. The architecture supports:

- Vertical slice organization with tests next to code
- Thai language utilities as core features
- Open core model for extensibility

## License

Licensed under the Elastic License 2.0. See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read the contributing guidelines and submit pull requests to the main branch.

## Support

For support and questions, please open an issue in the repository.