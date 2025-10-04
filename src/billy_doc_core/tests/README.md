# Billy Document Core - Integration Tests

This directory contains comprehensive integration tests for the billy-doc-core document generation API.

## Test Structure

### Files

- **`test_document_integration.py`** - Main integration tests that test end-to-end functionality
- **`conftest.py`** - Pytest configuration and shared fixtures
- **`run_integration_tests.py`** - Standalone test runner script

## Running Tests

### Option 1: Using pytest (Recommended)

```bash
# Run all tests
pytest src/billy_doc_core/tests/ -v

# Run only integration tests
pytest src/billy_doc_core/tests/ -v -m integration

# Run with coverage
pytest src/billy_doc_core/tests/ -v --cov=billy_doc_core

# Run specific test file
pytest src/billy_doc_core/tests/test_document_integration.py -v
```

### Option 2: Using the standalone runner

```bash
# From project root
python src/billy_doc_core/tests/run_integration_tests.py

# Or from tests directory
python run_integration_tests.py
```

### Option 3: Using the existing test script pattern

```bash
# Similar to your generate_doc.py script
cd src/billy_doc_core/tests
python run_integration_tests.py
```

## What Tests Cover

### ✅ Document Generation Tests

- **Quotation generation** with tax calculation and display
- **Invoice generation** with proper tax handling
- **Receipt generation** with tax breakdown
- **Multiple items** calculation verification
- **PDF content validation** (checks for correct amounts in PDF)

### ✅ Tax Calculation Tests

- **7% VAT calculation** for Thai business compliance
- **Subtotal calculation** from item totals
- **Tax line display** in PDF output
- **Final total verification** (subtotal + tax)

### ✅ API Response Tests

- **Response format validation** (document ID, number, download URL)
- **Document number format** (QT-*, INV-*, REC-*)
- **Status codes** (200 for success, 400/422 for errors)
- **Content-Type headers** for PDF downloads

### ✅ Error Handling Tests

- **Invalid document types** (returns 422)
- **Missing items** (returns 400)
- **Invalid numeric values** (proper error messages)
- **File not found** scenarios

### ✅ Content Validation Tests

- **PDF format verification** (valid PDF headers)
- **Text content extraction** (amounts appear in PDF)
- **Thai language support** (UTF-8 encoding)
- **Number formatting** (thousands separators, decimal places)

## Test Data

The tests use realistic Thai business data:

```python
# Sample quotation data
{
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
    ]
}
```

## Expected Results

### Quotation Test Results
- **Items**: 50,000 + 60,000 = **110,000** subtotal
- **Tax**: 110,000 × 7% = **7,700** VAT
- **Total**: **117,700** final amount
- **PDF contains**: All amounts in proper Thai format

### Invoice Test Results
- **Items**: 75,000 subtotal
- **Tax**: 75,000 × 7% = **5,250** VAT
- **Total**: **80,250** final amount

### Receipt Test Results
- **Items**: 30,000 subtotal
- **Tax**: 30,000 × 7% = **2,100** VAT
- **Total**: **32,100** final amount

## Prerequisites

1. **FastAPI server must be running**:
   ```bash
   uv run uvicorn src.billy_doc_core.main:app --reload
   ```

2. **Test assets must exist** (for logo/signature testing):
   - `src/billy_doc_core/assets/chongko_logo.png`
   - `src/billy_doc_core/assets/mager_logo.jpg`
   - `src/billy_doc_core/assets/warm_sign.jpg`

3. **Thai fonts must be installed** (for PDF generation):
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install fonts-sarabun

   # Or install manually to /usr/local/share/fonts/sarabun/
   ```

## Test Output

- **PDF files** are saved to `test_output/` directory for manual inspection
- **Test results** show detailed information about each test
- **Calculation verification** confirms mathematical accuracy
- **Content validation** ensures PDF contains expected text

## Manual Testing

You can also run your original script to manually verify:

```bash
cd billy-doc-core/local
python generate_doc.py
```

The integration tests complement your manual testing by providing automated verification of all the fixes we've implemented.

## Troubleshooting

### Common Issues

1. **Server not running**: Start the FastAPI server first
2. **Missing assets**: Ensure logo/signature files exist in assets directory
3. **Font issues**: Install Thai fonts for proper PDF rendering
4. **Port conflicts**: Ensure port 8000 is available

### Debug Mode

Run tests with verbose output for debugging:

```bash
pytest src/billy_doc_core/tests/ -v -s
```

## Integration with CI/CD

These tests can be integrated into your CI/CD pipeline:

```bash
# In your CI/CD script
pytest src/billy_doc_core/tests/test_document_integration.py -v
```

The tests are designed to be fast, reliable, and provide comprehensive coverage of the document generation functionality.