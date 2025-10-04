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


@pytest.fixture(scope="session", autouse=True)
def cleanup_all_generated_documents():
    """Automatically clean up all generated documents after all tests complete."""
    yield

    print("\n🧹 Running global cleanup of generated documents...")

    try:
        # Clean up test-specific output directory (primary location for test documents)
        test_output_dir = Path(__file__).parent / "test_output"
        if test_output_dir.exists():
            all_files = list(test_output_dir.glob("*"))
            pdf_files = [f for f in all_files if f.suffix.lower() == '.pdf']
            print(f"  📁 Found {len(pdf_files)} PDF files in test output directory")

            for pdf_file in pdf_files:
                try:
                    if pdf_file.exists():
                        pdf_file.unlink()
                        print(f"  🗑️ Deleted: {pdf_file.name}")
                    else:
                        print(f"  ⚠️ File not found: {pdf_file}")
                except PermissionError:
                    print(f"  ⚠️ Permission denied deleting {pdf_file}, trying again...")
                    try:
                        # Try to change permissions and delete
                        import stat
                        pdf_file.chmod(stat.S_IWRITE)
                        pdf_file.unlink()
                        print(f"  🗑️ Force deleted: {pdf_file.name}")
                    except Exception as e2:
                        print(f"  ❌ Could not delete {pdf_file}: {e2}")
                except Exception as e:
                    print(f"  ⚠️ Could not delete {pdf_file}: {e}")

            if pdf_files:
                print(f"  ✅ Cleaned up {len(pdf_files)} documents from test output directory")
            else:
                print("  ℹ️ No PDF documents found in test output directory")

        # Also clean up main output directory as backup
        main_output_dir = Path(__file__).parent.parent.parent / "output"
        if main_output_dir.exists():
            pdf_files = list(main_output_dir.glob("*.pdf"))
            if pdf_files:
                print(f"  📁 Found {len(pdf_files)} PDF files in main output directory (backup cleanup)")

                for pdf_file in pdf_files:
                    try:
                        pdf_file.unlink()
                        print(f"  🗑️ Deleted: {pdf_file.name}")
                    except Exception as e:
                        print(f"  ⚠️ Could not delete {pdf_file}: {e}")

                print(f"  ✅ Cleaned up {len(pdf_files)} documents from main output directory")

        # Clean up any test files created during tests
        test_assets_dir = Path(__file__).parent / "test_assets"
        if test_assets_dir.exists():
            all_files = list(test_assets_dir.glob("*"))
            print(f"  📁 Found {len(all_files)} files in test_assets directory")

            file_count = 0
            for file in all_files:
                try:
                    file.unlink()
                    file_count += 1
                except Exception as e:
                    print(f"  ⚠️ Could not delete test file {file}: {e}")
            try:
                test_assets_dir.rmdir()
                print(f"  ✅ Cleaned up test_assets directory ({file_count} files)")
            except Exception as e:
                print(f"  ⚠️ Could not remove test_assets directory: {e}")

        print("🧹 Global cleanup completed\n")

    except Exception as e:
        print(f"⚠️ Error during global cleanup: {e}")


def manual_cleanup():
    """Manual cleanup function that can be called directly if needed."""
    print("\n🔧 Running manual cleanup of generated documents...")

    try:
        # Clean up main output directory where documents are actually saved
        main_output_dir = Path(__file__).parent.parent.parent / "output"
        if main_output_dir.exists():
            pdf_files = list(main_output_dir.glob("*.pdf"))
            print(f"  📁 Found {len(pdf_files)} PDF files in main output directory")

            for pdf_file in pdf_files:
                try:
                    if pdf_file.exists():
                        pdf_file.unlink()
                        print(f"  🗑️ Deleted: {pdf_file.name}")
                except Exception as e:
                    print(f"  ⚠️ Could not delete {pdf_file}: {e}")

            if pdf_files:
                print(f"  ✅ Cleaned up {len(pdf_files)} documents from main output directory")
            else:
                print("  ℹ️ No documents found in main output directory")

        # Clean up test-specific output directory
        test_output_dir = Path(__file__).parent / "test_output"
        if test_output_dir.exists():
            pdf_files = list(test_output_dir.glob("*.pdf"))
            print(f"  📁 Found {len(pdf_files)} PDF files in test output directory")

            for pdf_file in pdf_files:
                try:
                    pdf_file.unlink()
                    print(f"  🗑️ Deleted: {pdf_file.name}")
                except Exception as e:
                    print(f"  ⚠️ Could not delete {pdf_file}: {e}")

            if pdf_files:
                print(f"  ✅ Cleaned up {len(pdf_files)} documents from test output directory")

        print("🔧 Manual cleanup completed\n")

    except Exception as e:
        print(f"⚠️ Error during manual cleanup: {e}")


# Add a command-line interface for manual cleanup
if __name__ == "__main__":
    manual_cleanup()


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