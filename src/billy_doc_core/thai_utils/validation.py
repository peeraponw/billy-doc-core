import re
from typing import List


class ThaiBusinessValidator:
    """Validator for Thai business terminology and standards."""

    # Thai business terms mapping
    BUSINESS_TERMS = {
        "invoice": "ใบแจ้งหนี้",
        "receipt": "ใบเสร็จรับเงิน",
        "quotation": "ใบเสนอราคา",
        "tax": "ภาษี",
        "vat": "ภาษีมูลค่าเพิ่ม",
        "company": "บริษัท",
        "limited": "จำกัด",
        "corporation": "มหาชน",
        "address": "ที่อยู่",
        "telephone": "โทรศัพท์",
        "email": "อีเมล",
        "customer": "ลูกค้า",
        "supplier": "ผู้จัดจำหน่าย",
        "payment": "การชำระเงิน",
        "bank": "ธนาคาร",
        "account": "บัญชี",
        "amount": "จำนวนเงิน",
        "total": "รวมทั้งสิ้น",
        "subtotal": "รวมเงิน",
        "discount": "ส่วนลด",
        "tax_id": "เลขประจำตัวผู้เสียภาษี",
    }

    # Thai tax ID pattern (13 digits)
    TAX_ID_PATTERN = re.compile(r'^\d{13}$')

    # Thai phone number patterns
    PHONE_PATTERNS = [
        re.compile(r'^0\d{8}$'),  # Mobile: 0XXXXXXXXX
        re.compile(r'^0\d{7}$'),  # Landline: 0XXXXXXX
        re.compile(r'^\d{2}-\d{3}-\d{4}$'),  # XX-XXX-XXXX
    ]

    # Thai business registration patterns
    BUSINESS_ID_PATTERNS = [
        re.compile(r'^\d{13}$'),  # Tax ID
        re.compile(r'^\d{10}$'),  # Company registration
    ]

    @classmethod
    def validate_tax_id(cls, tax_id: str) -> bool:
        """
        Validate Thai tax identification number.

        Args:
            tax_id: Tax ID to validate

        Returns:
            True if valid, False otherwise

        Raises:
            ValueError: If tax_id format is invalid
        """
        if not isinstance(tax_id, str):
            raise TypeError("Tax ID must be string")

        if not tax_id.strip():
            raise ValueError("Tax ID cannot be empty")

        if not cls.TAX_ID_PATTERN.match(tax_id):
            raise ValueError("Tax ID must be exactly 13 digits")

        # Thai tax ID checksum validation
        digits = [int(d) for d in tax_id]
        checksum = sum((i + 1) * digits[i] for i in range(12)) % 11
        check_digit = (11 - checksum) % 10

        if digits[12] != check_digit:
            raise ValueError("Invalid tax ID checksum")

        return True

    @classmethod
    def validate_phone_number(cls, phone: str) -> bool:
        """
        Validate Thai phone number format.

        Args:
            phone: Phone number to validate

        Returns:
            True if valid format, False otherwise

        Raises:
            ValueError: If phone format is invalid
        """
        if not isinstance(phone, str):
            raise TypeError("Phone number must be string")

        if not phone.strip():
            return False  # Optional field

        # Remove common separators
        clean_phone = re.sub(r'[\s\-\(\)]', '', phone)

        for pattern in cls.PHONE_PATTERNS:
            if pattern.match(clean_phone):
                return True

        raise ValueError("Invalid Thai phone number format")

    @classmethod
    def validate_business_name(cls, name: str) -> bool:
        """
        Validate Thai business name contains proper terminology.

        Args:
            name: Business name to validate

        Returns:
            True if contains valid Thai business terms, False otherwise

        Raises:
            ValueError: If name is invalid
        """
        if not isinstance(name, str):
            raise TypeError("Business name must be string")

        if not name.strip():
            raise ValueError("Business name cannot be empty")

        if len(name) > 200:
            raise ValueError("Business name too long (max 200 characters)")

        # Check for Thai business terms
        name_lower = name.lower()
        has_thai_terms = any(term in name_lower for term in cls.BUSINESS_TERMS.keys())

        if not has_thai_terms:
            raise ValueError("Business name should contain Thai business terminology")

        return True

    @classmethod
    def validate_thai_text(cls, text: str, field_name: str = "text") -> bool:
        """
        Validate Thai text input with proper error handling.

        Args:
            text: Thai text to validate
            field_name: Name of the field for error messages

        Returns:
            True if valid

        Raises:
            ValueError: If text is invalid
        """
        if not isinstance(text, str):
            raise TypeError(f"{field_name} must be string type")

        if not text or not text.strip():
            raise ValueError(f"{field_name} cannot be empty")

        # Remove any potentially harmful characters
        sanitized = text.strip()
        if len(sanitized) == 0:
            raise ValueError(f"{field_name} cannot be only whitespace")

        # Check for minimum Thai character content
        thai_chars = re.findall(r'[\u0E00-\u0E7F]', sanitized)
        if len(thai_chars) < len(sanitized) * 0.3:  # At least 30% Thai characters
            raise ValueError(f"{field_name} should contain Thai characters")

        return True

    @classmethod
    def get_business_term(cls, english_term: str) -> str:
        """
        Get Thai translation of English business term.

        Args:
            english_term: English business term

        Returns:
            Thai translation if available, otherwise original term
        """
        return cls.BUSINESS_TERMS.get(english_term.lower(), english_term)

    @classmethod
    def validate_document_standards(cls, document_data: dict) -> List[str]:
        """
        Validate document meets Thai business document standards.

        Args:
            document_data: Document data to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        try:
            # Validate required fields
            if 'customer_name' not in document_data or not document_data['customer_name']:
                errors.append("Required field 'customer_name' is missing")

            if 'document_type' not in document_data or not document_data['document_type']:
                errors.append("Required field 'document_type' is missing")

            # Validate customer name
            if 'customer_name' in document_data:
                try:
                    cls.validate_thai_text(document_data['customer_name'], 'customer_name')
                except ValueError as e:
                    errors.append(str(e))

            # Validate line amounts if provided
            if 'line_amounts' in document_data:
                for i, amount in enumerate(document_data['line_amounts']):
                    if not isinstance(amount, (int, float)):
                        errors.append(f"Line item {i+1} amount must be numeric, got {type(amount)}")
                    elif amount <= 0:
                        errors.append(f"Line item {i+1} amount must be positive")

            # Validate tax ID if provided
            if 'tax_id' in document_data and document_data['tax_id']:
                try:
                    cls.validate_tax_id(document_data['tax_id'])
                except ValueError as e:
                    errors.append(str(e))

            # Validate phone if provided
            if 'phone' in document_data and document_data['phone']:
                try:
                    cls.validate_phone_number(document_data['phone'])
                except ValueError as e:
                    errors.append(str(e))

            # Validate business name if provided
            if 'business_name' in document_data and document_data['business_name']:
                try:
                    cls.validate_business_name(document_data['business_name'])
                except ValueError as e:
                    errors.append(str(e))

        except Exception as e:
            errors.append(f"Validation error: {str(e)}")

        return errors