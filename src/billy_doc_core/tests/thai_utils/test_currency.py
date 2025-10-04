import pytest
from billy_doc_core.thai_utils.currency import thai_number_to_words


class TestThaiNumberToWords:
    """Test Thai number-to-words conversion."""

    def test_zero_amount(self):
        """Test zero amount conversion."""
        result = thai_number_to_words(0)
        assert result == "ศูนย์บาทถ้วน"

    def test_integer_amount(self):
        """Test integer amount conversion."""
        result = thai_number_to_words(100)
        assert result == "หนึ่งร้อยบาทถ้วน"

    def test_decimal_amount(self):
        """Test decimal amount conversion."""
        result = thai_number_to_words(123.50)
        assert result == "หนึ่งร้อยยี่สิบสามบาทห้าสิบสตางค์"

    def test_large_amount(self):
        """Test large amount conversion."""
        result = thai_number_to_words(1234.56)
        assert result == "หนึ่งพันสองร้อยสามสิบสี่บาทห้าสิบหกสตางค์"

    def test_invalid_amount_type(self):
        """Test that invalid amounts raise TypeError."""
        with pytest.raises(TypeError, match="Amount must be numeric"):
            thai_number_to_words("invalid")

    def test_negative_amount(self):
        """Test that negative amounts raise ValueError."""
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            thai_number_to_words(-100)

    def test_small_decimal(self):
        """Test small decimal amount."""
        result = thai_number_to_words(0.50)
        assert result == "ห้าสิบสตางค์"

    def test_million_amount(self):
        """Test million amount conversion."""
        result = thai_number_to_words(1000000)
        assert result == "หนึ่งล้านบาทถ้วน"