"""
Pytest configuration and fixtures for billy-doc-core tests.
"""

import pytest
import requests
from pathlib import Path


@pytest.fixture(scope="session")
def test_output_dir():
    """Provide test output directory for all tests."""
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    return output_dir


@pytest.fixture(scope="session")
def api_base_url():
    """Provide API base URL for tests."""
    return "http://localhost:8000/api/v1"


@pytest.fixture(scope="function")
def sample_quotation_data():
    """Provide sample quotation data for tests."""
    return {
        "document_type": "quotation",
        "customer_name": "นายสมชาย ใจดี",
        "customer_email": "somchai@example.com",
        "customer_address": "123 ถนนสุขุมวิท กรุงเทพฯ",
        "items": [
            {
                "description": "บริการพัฒนาเว็บไซต์",
                "qty": 1,
                "price": 50000.0
            },
            {
                "description": "บริการดูแลรักษา",
                "qty": 12,
                "price": 5000.0
            }
        ],
        "note": "โครงการพัฒนาระบบครบวงจร",
        "language": "th",
        "header_logo": "chongko_logo.png",
        "footer_logo": "mager_logo.jpg",
        "signature": "warm_sign.jpg"
    }


@pytest.fixture(scope="function")
def sample_invoice_data():
    """Provide sample invoice data for tests."""
    return {
        "document_type": "invoice",
        "customer_name": "บริษัท ตัวอย่าง จำกัด",
        "customer_email": "contact@example.com",
        "customer_address": "456 ถนนสีลม กรุงเทพฯ",
        "items": [
            {
                "description": "บริการให้คำปรึกษา",
                "qty": 1,
                "price": 75000.0
            }
        ],
        "note": "ใบแจ้งหนี้สำหรับการให้คำปรึกษา",
        "language": "th",
        "header_logo": "chongko_logo.png",
        "footer_logo": "mager_logo.jpg",
        "signature": "warm_sign.jpg"
    }


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )