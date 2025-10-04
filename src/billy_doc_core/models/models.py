from __future__ import annotations

from abc import ABC
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, computed_field


# ===== Enums =====

class OrderStatus(str, Enum):
    draft = "draft"
    quoted = "quoted"
    confirmed = "confirmed"
    invoiced = "invoiced"
    part_paid = "part_paid"
    paid = "paid"
    closed = "closed"
    void = "void"


class InvoiceStatus(str, Enum):
    draft = "draft"
    issued = "issued"
    overdue = "overdue"
    paid = "paid"
    void = "void"


class PaymentMethod(str, Enum):
    bank = "bank"
    card = "card"
    cash = "cash"
    other = "other"


class LineKind(str, Enum):
    product = "product"
    service = "service"
    discount = "discount"
    rounding = "rounding"
    note = "note"


class SourceType(str, Enum):
    manual = "manual"
    order_item = "order_item"


class Language(str, Enum):
    th = "th"
    en = "en"


# ===== Core =====

class Customer(BaseModel):
    id: str
    name: str
    address: Optional[str] = None
    email: Optional[str] = None
    tel: Optional[str] = None
    tax_id: Optional[str] = None


class Item(BaseModel):
    id: str
    order_id: str
    description: str
    qty: Decimal = Field(ge=Decimal("0"))
    price: Decimal = Field(ge=Decimal("0"))

    @computed_field
    @property
    def total(self) -> Decimal:
        return (self.qty * self.price).quantize(Decimal("0.01"))


class Order(BaseModel):
    id: str
    customer_id: str
    currency: str = "THB"
    created_at: datetime
    is_tax_inclusive: bool = False
    tax_rate: Optional[Decimal] = Field(default=None, ge=Decimal("0"))
    items: List[Item] = []
    note: Optional[str] = None
    status: OrderStatus = OrderStatus.draft

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        return sum((i.total for i in self.items), Decimal("0.00"))

    @computed_field
    @property
    def tax_amount(self) -> Decimal:
        if not self.tax_rate:
            return Decimal("0.00")
        if self.is_tax_inclusive:
            g = self.subtotal
            r = self.tax_rate
            return (g - (g / (Decimal("1") + r))).quantize(Decimal("0.01"))
        return (self.subtotal * self.tax_rate).quantize(Decimal("0.01"))

    @computed_field
    @property
    def total(self) -> Decimal:
        if self.is_tax_inclusive:
            return self.subtotal
        return (self.subtotal + self.tax_amount).quantize(Decimal("0.01"))


# ===== Company snapshot (versioned on each document) =====

class CompanySnapshot(BaseModel):
    name: str
    address_1: str
    address_2: str
    tel: str
    tax_id: str
    bank_account: str
    header_logo: str
    footer_logo: str
    signature: Optional[str] = None  # e.g., key to a rendered signature asset


# ===== Document building blocks =====

class DocumentTotals(BaseModel):
    currency: str
    subtotal: Decimal = Field(ge=Decimal("0"))
    tax: Decimal = Field(ge=Decimal("0"))
    total: Decimal = Field(ge=Decimal("0"))


class DocumentLine(BaseModel):
    """Reusable line for quotations and invoices."""
    id: str
    order_item_id: Optional[str] = None
    kind: LineKind = LineKind.product
    source_type: SourceType = SourceType.manual
    source_id: Optional[str] = None
    description: str
    qty: Optional[Decimal] = Field(default=None, ge=Decimal("0"))
    unit_price: Optional[Decimal] = Field(default=None)
    tax_rate: Optional[Decimal] = Field(default=None, ge=Decimal("0"))
    line_total: Decimal = Field(ge=Decimal("0"))  # snapshot after rounding


# ===== Documents (immutable snapshots) =====

class BaseDocument(BaseModel, ABC):
    id: str
    document_no: str
    issue_date: date
    order_id: str
    company: CompanySnapshot
    note: Optional[str] = None
    language: Language = Language.th


class QuotationDoc(BaseDocument):
    valid_until: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    scope: Optional[str] = None
    deliverables: Optional[str] = None
    payment_terms: Optional[str] = None
    lines: List[DocumentLine]
    totals: DocumentTotals


class InvoiceDoc(BaseDocument):
    due_date: Optional[date] = None
    status: InvoiceStatus = InvoiceStatus.draft
    lines: List[DocumentLine]
    totals: DocumentTotals


class ReceiptDoc(BaseDocument):
    allocation_ids: List[str]  # provenance to allocations
    amount_total: Decimal = Field(ge=Decimal("0"))


# ===== Payments and allocations (ledger layer) =====

class Payment(BaseModel):
    id: str
    order_id: str
    customer_id: str
    received_date: date
    method: PaymentMethod = PaymentMethod.bank
    currency: str = "THB"
    amount: Decimal = Field(ge=Decimal("0"))
    note: Optional[str] = None


class PaymentAllocation(BaseModel):
    id: str
    payment_id: str
    invoice_id: str
    amount: Decimal = Field(ge=Decimal("0"))
    created_at: datetime


# ===== API Request/Response Models =====

class DocumentGenerateRequest(BaseModel):
    document_type: str = Field(..., pattern="^(quotation|invoice|receipt)$")
    customer_name: str = Field(..., min_length=1, max_length=200)
    customer_email: Optional[str] = None
    customer_address: Optional[str] = None
    items: List[dict] = Field(..., min_items=1)
    note: Optional[str] = None
    language: Language = Language.th
    header_logo: str = "blank.png"
    footer_logo: str = "blank.png"
    signature: str = "blank.png"

class DocumentResponse(BaseModel):
    id: str
    document_no: str
    document_type: str
    status: str
    download_url: str
    created_at: datetime