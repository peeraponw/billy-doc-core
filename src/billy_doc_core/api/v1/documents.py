import uuid
from datetime import date, datetime
from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from pydantic import ValidationError

from billy_doc_core.models.models import (
    DocumentGenerateRequest,
    DocumentResponse,
    QuotationDoc,
    InvoiceDoc,
    ReceiptDoc,
    Customer,
    CompanySnapshot,
    DocumentLine,
    DocumentTotals,
)
from billy_doc_core.services.document_service import DocumentService
from billy_doc_core.thai_utils.validation import ThaiBusinessValidator
from billy_doc_core.const import (
    DEFAULT_COMPANY,
    DEFAULT_TAX_RATE,
    THAI_BAHT_CURRENCY,
)

router = APIRouter()
document_service = DocumentService()


@router.post("/documents/generate", response_model=DocumentResponse)
async def generate_document(request: DocumentGenerateRequest):
    """Generate a new document (quotation, invoice, or receipt)."""
    try:
        # Validate Thai business standards
        validation_errors = ThaiBusinessValidator.validate_document_standards({
            "customer_name": request.customer_name,
            "amount": sum(item.get("qty", 1) * item.get("price", 0) for item in request.items),
            "document_type": request.document_type,
        })

        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Validation errors: {'; '.join(validation_errors)}"
            )

        # Validate Thai text input
        try:
            ThaiBusinessValidator.validate_thai_text(request.customer_name, "customer_name")
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

        if not request.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one item is required"
            )

        # Generate document ID
        document_id = str(uuid.uuid4())

        # Create customer
        customer = Customer(
            id=str(uuid.uuid4()),
            name=request.customer_name,
            email=request.customer_email,
            address=request.customer_address,
        )

        # Create document lines
        lines = []
        subtotal = 0
        for item in request.items:
            line_id = str(uuid.uuid4())
            qty = item.get("qty", 1)
            price = item.get("price", 0)
            line_total = qty * price
            subtotal += line_total

            line = DocumentLine(
                id=line_id,
                description=item.get("description", ""),
                qty=qty,
                unit_price=price,
                line_total=line_total,
            )
            lines.append(line)

        # Calculate totals
        tax_rate = DEFAULT_TAX_RATE
        tax_amount = subtotal * tax_rate
        total = subtotal + tax_amount

        totals = DocumentTotals(
            currency=THAI_BAHT_CURRENCY,
            subtotal=subtotal,
            tax=tax_amount,
            total=total,
        )

        # Create company snapshot from constants
        company = CompanySnapshot(**DEFAULT_COMPANY)

        # Create document based on type
        if request.document_type == "quotation":
            document = QuotationDoc(
                id=document_id,
                document_no=f"QT-{document_id[:8]}",
                issue_date=date.today(),
                order_id=str(uuid.uuid4()),
                company=company,
                note=request.note,
                language=request.language,
                lines=lines,
                totals=totals,
            )
            pdf_bytes = await document_service.generate_quotation_pdf(document)

        elif request.document_type == "invoice":
            document = InvoiceDoc(
                id=document_id,
                document_no=f"INV-{document_id[:8]}",
                issue_date=date.today(),
                order_id=str(uuid.uuid4()),
                company=company,
                note=request.note,
                language=request.language,
                lines=lines,
                totals=totals,
            )
            pdf_bytes = await document_service.generate_invoice_pdf(document)

        elif request.document_type == "receipt":
            document = ReceiptDoc(
                id=document_id,
                document_no=f"REC-{document_id[:8]}",
                issue_date=date.today(),
                order_id=str(uuid.uuid4()),
                company=company,
                note=request.note,
                language=request.language,
                allocation_ids=[],
                amount_total=total,
            )
            pdf_bytes = await document_service.generate_receipt_pdf(document)

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid document type"
            )

        # Save document
        file_path = document_service.save_document(document_id, pdf_bytes)

        # Return response
        return DocumentResponse(
            id=document_id,
            document_no=document.document_no,
            document_type=request.document_type,
            status="generated",
            download_url=f"/api/documents/{document_id}",
            created_at=datetime.now(),
        )

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document generation failed: {str(e)}"
        )


@router.get("/documents/{document_id}")
async def get_document(document_id: str):
    """Retrieve a generated document."""
    try:
        pdf_bytes = document_service.get_document(document_id)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={document_id}.pdf"}
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving document: {str(e)}"
        )


@router.get("/documents")
async def list_documents():
    """List all generated documents."""
    try:
        documents = document_service.list_documents()
        return {"documents": documents, "total": len(documents)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing documents: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint for document service."""
    try:
        health = document_service.health_check()
        if health["status"] == "healthy":
            return health
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service unhealthy"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}"
        )