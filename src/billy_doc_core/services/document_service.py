import base64
import os
import time
import uuid
from datetime import date, datetime
from io import BytesIO
from pathlib import Path
from typing import Union, Dict, Any

from jinja2 import Environment, FileSystemLoader
from weasyprint import CSS, HTML
from weasyprint.text.fonts import FontConfiguration

from billy_doc_core.models.models import QuotationDoc, InvoiceDoc, ReceiptDoc, Customer, CompanySnapshot
from billy_doc_core.thai_utils.currency import thai_number_to_words
from billy_doc_core.thai_utils.date import format_thai_date
from billy_doc_core.const import OUTPUT_DIR, MAX_FILE_SIZE


class DocumentService:
    """Service for generating and managing PDF documents."""

    def __init__(self):
        """Initialize the DocumentService."""
        self.font_config = FontConfiguration()
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.assets_dir = Path(__file__).parent.parent / "assets"
        self.output_dir = Path(__file__).parent.parent.parent.parent / "output"

        # Ensure directories exist
        self.templates_dir.mkdir(exist_ok=True)
        self.assets_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)

        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
        self.env.filters["number_to_thai_text"] = thai_number_to_words
        self.env.filters["format_date_thai_eng"] = format_thai_date

    def _get_image_data_url(self, image_path: str) -> str:
        """Convert image file to data URL with support for PNG and JPG."""
        if not image_path or image_path == "blank.png":
            return ""

        # Check if assets directory exists and is accessible
        if not self.assets_dir.exists():
            raise FileNotFoundError(f"Assets directory not found: {self.assets_dir}")

        if not os.access(self.assets_dir, os.R_OK):
            raise PermissionError(f"Permission denied accessing assets directory: {self.assets_dir}")

        full_path = self.assets_dir / image_path

        # Check if file exists
        if not full_path.exists():
            raise FileNotFoundError(f"Asset file not found: {image_path}")

        # Check file size before reading
        file_size = full_path.stat().st_size
        if file_size > MAX_FILE_SIZE:
            raise ValueError(f"Asset file too large: {image_path} ({file_size} bytes) exceeds maximum allowed size {MAX_FILE_SIZE}")

        # Check if file is readable
        if not os.access(full_path, os.R_OK):
            raise PermissionError(f"Permission denied accessing asset file: {image_path}")

        with open(full_path, "rb") as img_file:
            file_content = img_file.read()
            encoded = base64.b64encode(file_content).decode()

            # Determine MIME type based on file extension
            if image_path.lower().endswith('.png'):
                mime_type = "image/png"
            elif image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
                mime_type = "image/jpeg"
            else:
                raise ValueError(f"Unsupported image format: {image_path}. Supported formats: PNG, JPG, JPEG")

            return f"data:{mime_type};base64,{encoded}"

    async def _generate_pdf(
        self, template_name: str, data: Union[QuotationDoc, InvoiceDoc, ReceiptDoc], customer: Customer, items: list
    ) -> bytes:
        """Generic PDF generation method matching example pattern."""
        template = self.env.get_template(template_name)

        # Process signature image
        signature_image = ""
        if data.company.signature:
            signature_image = self._get_image_data_url(data.company.signature)

        # Process header and footer logos
        header_logo = self._get_image_data_url(data.company.header_logo)
        footer_logo = self._get_image_data_url(data.company.footer_logo)

        context = {
            "data": data,
            "company_config": data.company,
            "customer": customer,
            "items": items,
            "signature_image": signature_image,
            "header_logo": header_logo,
            "footer_logo": footer_logo,
            "current_date": date.today(),
        }

        html_content = template.render(context)

        html = HTML(string=html_content, base_url=str(self.assets_dir))
        css = CSS(
            string="""
            @font-face {
                font-family: 'Sarabun';
                src: url('file:///usr/local/share/fonts/sarabun/Sarabun-Regular.ttf') format('truetype');
                font-weight: normal;
            }
            @font-face {
                font-family: 'Sarabun';
                src: url('file:///usr/local/share/fonts/sarabun/Sarabun-Bold.ttf') format('truetype');
                font-weight: bold;
            }
            """,
            font_config=self.font_config,
        )
        pdf_buffer = BytesIO()
        html.write_pdf(pdf_buffer, stylesheets=[css], font_config=self.font_config)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()

    def _get_default_company(self) -> CompanySnapshot:
        """Get default company snapshot for testing."""
        return CompanySnapshot(
            name="บริษัท บิลลี่ ด็อก จำกัด",
            address_1="123 ถนนสุขุมวิท",
            address_2="แขวงคลองเตย เขตคลองเตย กรุงเทพฯ 10110",
            tel="02-123-4567",
            tax_id="0123456789012",
            bank_account="123-4-56789-0",
            header_logo="",
            footer_logo="",
        )

    async def generate_quotation_pdf(self, quotation: QuotationDoc, customer: Customer, items: list) -> bytes:
        """Generate PDF for a quotation."""
        return await self._generate_pdf("quotation.html", quotation, customer, items)

    async def generate_invoice_pdf(self, invoice: InvoiceDoc, customer: Customer, items: list) -> bytes:
        """Generate PDF for an invoice."""
        return await self._generate_pdf("invoice.html", invoice, customer, items)

    async def generate_receipt_pdf(self, receipt: ReceiptDoc, customer: Customer, items: list) -> bytes:
        """Generate PDF for a receipt."""
        return await self._generate_pdf("receipt.html", receipt, customer, items)

    def save_document(self, document_id: str, pdf_bytes: bytes) -> str:
        """Save PDF document to file system with performance monitoring."""
        start_time = time.time()

        # Validate file size
        if len(pdf_bytes) > MAX_FILE_SIZE:
            raise ValueError(f"PDF file size {len(pdf_bytes)} exceeds maximum allowed size {MAX_FILE_SIZE}")

        file_path = self.output_dir / f"{document_id}.pdf"

        try:
            with open(file_path, "wb") as f:
                f.write(pdf_bytes)

            save_time = time.time() - start_time

            # Log performance metrics
            print(f"Document {document_id} saved in {save_time:.3f} seconds")

            return str(file_path)

        except Exception as e:
            raise ValueError(f"Failed to save document {document_id}: {str(e)}")

    def get_document(self, document_id: str) -> bytes:
        """Retrieve PDF document from file system."""
        file_path = self.output_dir / f"{document_id}.pdf"
        if not file_path.exists():
            raise FileNotFoundError(f"Document {document_id} not found")
        with open(file_path, "rb") as f:
            return f.read()

    def list_documents(self) -> list:
        """List all saved documents."""
        documents = []
        for pdf_file in self.output_dir.glob("*.pdf"):
            doc_id = pdf_file.stem
            stat = pdf_file.stat()
            documents.append({
                "id": doc_id,
                "filename": pdf_file.name,
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            })
        return documents

    def health_check(self) -> Dict[str, Any]:
        """Perform health check for the document service."""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }

        try:
            # Check if output directory exists and is writable
            if not self.output_dir.exists():
                health_status["status"] = "unhealthy"
                health_status["checks"]["output_directory"] = "Directory does not exist"
            elif not os.access(self.output_dir, os.W_OK):
                health_status["status"] = "unhealthy"
                health_status["checks"]["output_directory"] = "Directory not writable"
            else:
                health_status["checks"]["output_directory"] = "OK"

            # Check if templates directory exists
            if not self.templates_dir.exists():
                health_status["status"] = "unhealthy"
                health_status["checks"]["templates_directory"] = "Directory does not exist"
            else:
                health_status["checks"]["templates_directory"] = "OK"

            # Check document count
            document_count = len(list(self.output_dir.glob("*.pdf")))
            health_status["checks"]["document_count"] = document_count

            # Check average file size
            total_size = sum(f.stat().st_size for f in self.output_dir.glob("*.pdf"))
            avg_size = total_size / max(document_count, 1)
            health_status["checks"]["average_file_size"] = avg_size

        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["error"] = str(e)

        return health_status